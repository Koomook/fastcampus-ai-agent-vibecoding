#!/bin/bash
# Test Slack app_mention event using curl with valid signature

SLACK_SIGNING_SECRET="50703281a14f1ba85172173b65b4d2a9"
URL="https://slack-claude-bot-806381030765.us-central1.run.app/slack/events"
TIMESTAMP=$(date +%s)

# Event payload
PAYLOAD='{
  "token": "test_token",
  "team_id": "T01234567",
  "api_app_id": "A01234567",
  "event": {
    "type": "app_mention",
    "user": "U01234567",
    "text": "<@U0BOTUSER> What is Python? Explain briefly.",
    "ts": "1234567890.123456",
    "channel": "C01234567",
    "event_ts": "1234567890.123456"
  },
  "type": "event_callback",
  "event_id": "Ev01234567",
  "event_time": '$TIMESTAMP'
}'

# Generate signature
SIG_BASESTRING="v0:$TIMESTAMP:$PAYLOAD"
SIGNATURE="v0=$(echo -n "$SIG_BASESTRING" | openssl dgst -sha256 -hmac "$SLACK_SIGNING_SECRET" | awk '{print $2}')"

echo "📤 Sending test event with curl..."
echo "⏰ Timestamp: $TIMESTAMP"
echo "🔐 Signature: $SIGNATURE"
echo ""

# Send request
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "X-Slack-Request-Timestamp: $TIMESTAMP" \
  -H "X-Slack-Signature: $SIGNATURE" \
  -d "$PAYLOAD")

HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
BODY=$(echo "$RESPONSE" | head -n -1)

echo "✅ HTTP Status: $HTTP_CODE"
echo "📥 Response Body: $BODY"

if [ "$HTTP_CODE" = "200" ]; then
  echo ""
  echo "✅ Test successful!"
  echo "   The bot is processing the message in background."
  exit 0
else
  echo ""
  echo "❌ Test failed with status code: $HTTP_CODE"
  exit 1
fi
