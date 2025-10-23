#!/usr/bin/env python3
"""
Test script to simulate Slack app_mention event with valid signature
"""
import hashlib
import hmac
import json
import time
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# Configuration
SLACK_SIGNING_SECRET = "50703281a14f1ba85172173b65b4d2a9"
CLOUD_RUN_URL = "https://slack-claude-bot-806381030765.us-central1.run.app/slack/events"

# Slack app_mention event payload
event_payload = {
    "token": "test_token",
    "team_id": "T01234567",
    "api_app_id": "A01234567",
    "event": {
        "type": "app_mention",
        "user": "U01234567",
        "text": "<@U0BOTUSER> Hello! Can you help me with Python?",
        "ts": "1234567890.123456",
        "channel": "C01234567",
        "event_ts": "1234567890.123456"
    },
    "type": "event_callback",
    "event_id": "Ev01234567",
    "event_time": int(time.time())
}

def generate_slack_signature(body: str, timestamp: str, signing_secret: str) -> str:
    """Generate Slack request signature"""
    sig_basestring = f"v0:{timestamp}:{body}"
    signature = "v0=" + hmac.new(
        signing_secret.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature

def test_slack_event(url: str):
    """Send test app_mention event to Cloud Run endpoint"""
    # Prepare request
    timestamp = str(int(time.time()))
    body = json.dumps(event_payload)
    signature = generate_slack_signature(body, timestamp, SLACK_SIGNING_SECRET)

    print(f"📤 Sending test app_mention event to: {url}")
    print(f"⏰ Timestamp: {timestamp}")
    print(f"🔐 Signature: {signature}")
    print(f"📦 Payload: {json.dumps(event_payload, indent=2)}\n")

    # Create request
    headers = {
        "Content-Type": "application/json",
        "X-Slack-Request-Timestamp": timestamp,
        "X-Slack-Signature": signature,
    }

    req = Request(
        url,
        data=body.encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        # Send request
        with urlopen(req, timeout=10) as response:
            status_code = response.status
            response_body = response.read().decode("utf-8")

            print(f"✅ Response Status: {status_code}")
            print(f"📥 Response Body: {response_body}")

            if status_code == 200:
                print("\n✅ Test successful! Check your Slack channel for the bot's response.")
                print("   (The bot processes the message in background, so it may take a few seconds)")
                return True
            else:
                print(f"\n❌ Unexpected status code: {status_code}")
                return False

    except HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        print(f"   Response: {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else CLOUD_RUN_URL
    success = test_slack_event(url)
    sys.exit(0 if success else 1)
