"""
Slack Claude Bot - Main FastAPI Application
Phase 2: Claude Agent SDK Integration
Phase 3: Notion MCP Integration
"""
import hashlib
import hmac
import json
import logging
import time
from typing import Any

from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from claude_service import ClaudeService, convert_slack_history_to_claude_messages
from config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}',
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Slack Claude Bot", version="0.2.0")

# Initialize Slack client
slack_client = WebClient(token=settings.SLACK_BOT_TOKEN)

# Initialize Claude service with Notion MCP if token available
notion_token = settings.NOTION_TOKEN if settings.NOTION_TOKEN else None
claude_service = ClaudeService(notion_token=notion_token)


def verify_slack_signature(
    body: bytes,
    timestamp: str,
    signature: str,
) -> bool:
    """
    Verify Slack request signature.
    Reference: https://api.slack.com/authentication/verifying-requests-from-slack
    """
    # Check timestamp to prevent replay attacks (5 minutes tolerance)
    current_timestamp = int(time.time())
    if abs(current_timestamp - int(timestamp)) > 60 * 5:
        logger.warning(f"Request timestamp too old: {timestamp}")
        return False

    # Create signature base string
    sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"

    # Compute HMAC-SHA256 signature
    computed_signature = (
        "v0="
        + hmac.new(
            settings.SLACK_SIGNING_SECRET.encode(),
            sig_basestring.encode(),
            hashlib.sha256,
        ).hexdigest()
    )

    # Compare signatures
    return hmac.compare_digest(computed_signature, signature)


async def process_app_mention(event_data: dict[str, Any]) -> None:
    """
    Process app_mention event in background.
    Phase 2: Use Claude Agent SDK to generate intelligent responses.
    """
    start_time = time.time()
    thinking_message_ts = None

    try:
        event = event_data.get("event", {})
        channel = event.get("channel")
        thread_ts = event.get("thread_ts") or event.get("ts")
        user = event.get("user")
        user_message = event.get("text", "")

        logger.info(
            json.dumps(
                {
                    "action": "processing_mention",
                    "channel": channel,
                    "thread_ts": thread_ts,
                    "user": user,
                    "message_preview": user_message[:100],
                }
            )
        )

        # Send "Thinking..." message to show activity
        thinking_response = slack_client.chat_postMessage(
            channel=channel,
            thread_ts=thread_ts,
            text="🤔 Thinking...",
        )
        thinking_message_ts = thinking_response.get("ts")

        # Fetch thread history for context (up to 15 messages)
        try:
            history_response = slack_client.conversations_replies(
                channel=channel,
                ts=thread_ts,
                limit=15,
            )
            slack_messages = history_response.get("messages", [])
        except SlackApiError as e:
            if e.response and e.response.get("error") == "rate_limited":
                logger.warning("Rate limited on conversations_replies, using current message only")
                slack_messages = [{"user": user, "text": user_message}]
            else:
                raise

        # Convert Slack messages to Claude format
        conversation_history = convert_slack_history_to_claude_messages(slack_messages)

        # Process with Claude
        logger.info(
            json.dumps(
                {
                    "action": "claude_request_start",
                    "history_length": len(conversation_history),
                }
            )
        )

        claude_response = await claude_service.process_message(
            user_message,
            conversation_history=conversation_history if len(conversation_history) > 0 else None,
        )

        # Extract response text
        response_text = claude_response.get("response", "")
        tokens = claude_response.get("tokens", {})
        tool_uses = claude_response.get("tool_uses", [])
        elapsed_time = time.time() - start_time

        logger.info(
            json.dumps(
                {
                    "action": "claude_response_received",
                    "input_tokens": tokens.get("input", 0),
                    "output_tokens": tokens.get("output", 0),
                    "tool_uses_count": len(tool_uses),
                    "elapsed_seconds": round(elapsed_time, 2),
                }
            )
        )

        # Show tool usage in thread if any tools were used
        if tool_uses:
            tool_usage_text = "🔍 *Knowledge Base Searches:*\n"
            for i, tool_use in enumerate(tool_uses, 1):
                tool_name = tool_use.get("name", "unknown")
                tool_input = tool_use.get("input", {})
                tool_usage_text += f"{i}. `{tool_name}` - {json.dumps(tool_input, ensure_ascii=False)}\n"

            # Post tool usage as separate message
            slack_client.chat_postMessage(
                channel=channel,
                thread_ts=thread_ts,
                text=tool_usage_text,
            )

        # Format response with metadata
        metadata_parts = [
            f"Processing time: {elapsed_time:.1f}s",
            f"Tokens: {tokens.get('input', 0)} in, {tokens.get('output', 0)} out",
        ]

        if tool_uses:
            metadata_parts.append(f"Tools used: {len(tool_uses)}")

        formatted_response = f"{response_text}\n\n_{' | '.join(metadata_parts)}_"

        # Update thinking message with final response
        slack_client.chat_update(
            channel=channel,
            ts=thinking_message_ts,
            text=formatted_response,
        )

        logger.info(
            json.dumps(
                {
                    "action": "response_updated",
                    "channel": channel,
                    "thread_ts": thread_ts,
                    "message_ts": thinking_message_ts,
                }
            )
        )

    except SlackApiError as e:
        error_msg = f"Slack API Error: {e.response.get('error') if e.response else str(e)}"
        logger.error(
            json.dumps(
                {
                    "error": "slack_api_error",
                    "error_message": str(e),
                    "response": e.response.get("error") if e.response else None,
                }
            )
        )

        # Try to update thinking message with error
        if thinking_message_ts:
            try:
                slack_client.chat_update(
                    channel=channel,
                    ts=thinking_message_ts,
                    text=f"❌ {error_msg}",
                )
            except SlackApiError:
                pass

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        logger.error(
            json.dumps(
                {
                    "error": "unexpected_error",
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                }
            )
        )

        # Try to update thinking message with error
        if thinking_message_ts:
            try:
                slack_client.chat_update(
                    channel=channel,
                    ts=thinking_message_ts,
                    text=f"❌ {error_msg}",
                )
            except SlackApiError:
                pass


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for Cloud Run."""
    return {"status": "ok"}


@app.post("/slack/events")
async def slack_events(
    request: Request,
    background_tasks: BackgroundTasks,
    x_slack_request_timestamp: str = Header(..., alias="X-Slack-Request-Timestamp"),
    x_slack_signature: str = Header(..., alias="X-Slack-Signature"),
) -> Response:
    """
    Handle Slack event subscriptions.
    Reference: https://api.slack.com/events-api
    """
    # Get raw body for signature verification
    body = await request.body()

    # Verify Slack signature
    if not verify_slack_signature(body, x_slack_request_timestamp, x_slack_signature):
        logger.warning("Invalid Slack signature")
        raise HTTPException(status_code=403, detail="Invalid signature")

    # Parse JSON body
    try:
        event_data = json.loads(body)
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body")
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Handle URL verification challenge
    # Reference: https://api.slack.com/events/url_verification
    if event_data.get("type") == "url_verification":
        logger.info("Handling URL verification challenge")
        return JSONResponse(
            content={"challenge": event_data.get("challenge")},
            headers={"Content-Type": "application/json"},
        )

    # Handle app_mention event
    event = event_data.get("event", {})
    if event.get("type") == "app_mention":
        # Ignore bot's own messages
        if event.get("bot_id"):
            return Response(status_code=200)

        # Process mention in background to meet 3-second timeout
        background_tasks.add_task(process_app_mention, event_data)
        return Response(status_code=200)

    # Return 200 for other events
    return Response(status_code=200)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
