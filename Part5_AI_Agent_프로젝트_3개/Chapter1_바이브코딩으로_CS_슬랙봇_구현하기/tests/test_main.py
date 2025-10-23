"""
Unit tests for main FastAPI application.
Tests signature verification, URL verification, and event handling.
"""
import hashlib
import hmac
import json
import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app, verify_slack_signature


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_slack_client():
    """Mock Slack WebClient."""
    with patch("main.slack_client") as mock:
        mock.chat_postMessage = MagicMock(return_value={"ok": True, "ts": "1234567890.123456"})
        yield mock


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self, client):
        """Test GET /health returns 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestSlackSignatureVerification:
    """Test Slack signature verification."""

    def test_verify_slack_signature_valid(self):
        """Test signature verification with valid signature."""
        timestamp = str(int(time.time()))
        body = b'{"type": "url_verification", "challenge": "test_challenge"}'

        # Create valid signature
        sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
        from config import settings
        signature = "v0=" + hmac.new(
            settings.SLACK_SIGNING_SECRET.encode(),
            sig_basestring.encode(),
            hashlib.sha256,
        ).hexdigest()

        assert verify_slack_signature(body, timestamp, signature) is True

    def test_verify_slack_signature_invalid(self):
        """Test signature verification with invalid signature."""
        timestamp = str(int(time.time()))
        body = b'{"type": "url_verification"}'
        invalid_signature = "v0=invalid_signature"

        assert verify_slack_signature(body, timestamp, invalid_signature) is False

    def test_verify_slack_signature_old_timestamp(self):
        """Test signature verification rejects old timestamps."""
        # Timestamp from 10 minutes ago
        old_timestamp = str(int(time.time()) - 600)
        body = b'{"type": "url_verification"}'

        # Even with valid signature, old timestamp should fail
        sig_basestring = f"v0:{old_timestamp}:{body.decode('utf-8')}"
        from config import settings
        signature = "v0=" + hmac.new(
            settings.SLACK_SIGNING_SECRET.encode(),
            sig_basestring.encode(),
            hashlib.sha256,
        ).hexdigest()

        assert verify_slack_signature(body, old_timestamp, signature) is False


class TestURLVerification:
    """Test Slack URL verification challenge."""

    def test_url_verification_challenge(self, client):
        """Test URL verification returns challenge parameter."""
        timestamp = str(int(time.time()))
        challenge = "test_challenge_123"
        body = json.dumps({
            "type": "url_verification",
            "challenge": challenge,
        })

        # Create valid signature
        sig_basestring = f"v0:{timestamp}:{body}"
        from config import settings
        signature = "v0=" + hmac.new(
            settings.SLACK_SIGNING_SECRET.encode(),
            sig_basestring.encode(),
            hashlib.sha256,
        ).hexdigest()

        response = client.post(
            "/slack/events",
            content=body,
            headers={
                "X-Slack-Request-Timestamp": timestamp,
                "X-Slack-Signature": signature,
                "Content-Type": "application/json",
            },
        )

        assert response.status_code == 200
        assert response.json() == {"challenge": challenge}

    def test_url_verification_invalid_signature(self, client):
        """Test URL verification rejects invalid signature."""
        timestamp = str(int(time.time()))
        body = json.dumps({
            "type": "url_verification",
            "challenge": "test_challenge",
        })

        response = client.post(
            "/slack/events",
            content=body,
            headers={
                "X-Slack-Request-Timestamp": timestamp,
                "X-Slack-Signature": "v0=invalid",
                "Content-Type": "application/json",
            },
        )

        assert response.status_code == 403


class TestAppMentionEvent:
    """Test app_mention event handling."""

    def test_app_mention_event(self, client, mock_slack_client):
        """Test app_mention event triggers Claude response."""
        timestamp = str(int(time.time()))
        body = json.dumps({
            "type": "event_callback",
            "event": {
                "type": "app_mention",
                "user": "U123456",
                "text": "<@UBOT> hello",
                "channel": "C123456",
                "ts": "1234567890.123456",
            },
        })

        # Create valid signature
        sig_basestring = f"v0:{timestamp}:{body}"
        from config import settings
        signature = "v0=" + hmac.new(
            settings.SLACK_SIGNING_SECRET.encode(),
            sig_basestring.encode(),
            hashlib.sha256,
        ).hexdigest()

        # Mock chat_postMessage to return thinking message
        mock_slack_client.chat_postMessage.return_value = {
            "ok": True,
            "ts": "1234567890.999999"
        }

        # Mock conversations_replies to return empty history
        mock_slack_client.conversations_replies.return_value = {
            "messages": [
                {"user": "U123456", "text": "<@UBOT> hello"},
            ]
        }

        response = client.post(
            "/slack/events",
            content=body,
            headers={
                "X-Slack-Request-Timestamp": timestamp,
                "X-Slack-Signature": signature,
                "Content-Type": "application/json",
            },
        )

        # Should return 200 immediately
        assert response.status_code == 200

    def test_app_mention_ignores_bot_messages(self, client, mock_slack_client):
        """Test app_mention ignores messages from bots."""
        timestamp = str(int(time.time()))
        body = json.dumps({
            "type": "event_callback",
            "event": {
                "type": "app_mention",
                "user": "U123456",
                "bot_id": "B123456",  # Bot message
                "text": "<@UBOT> hello",
                "channel": "C123456",
                "ts": "1234567890.123456",
            },
        })

        # Create valid signature
        sig_basestring = f"v0:{timestamp}:{body}"
        from config import settings
        signature = "v0=" + hmac.new(
            settings.SLACK_SIGNING_SECRET.encode(),
            sig_basestring.encode(),
            hashlib.sha256,
        ).hexdigest()

        response = client.post(
            "/slack/events",
            content=body,
            headers={
                "X-Slack-Request-Timestamp": timestamp,
                "X-Slack-Signature": signature,
                "Content-Type": "application/json",
            },
        )

        assert response.status_code == 200
        # Should not call chat_postMessage for bot messages
        mock_slack_client.chat_postMessage.assert_not_called()

    def test_invalid_json_returns_400(self, client):
        """Test invalid JSON returns 400 error."""
        timestamp = str(int(time.time()))
        body = b"invalid json"

        # Create valid signature
        sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
        from config import settings
        signature = "v0=" + hmac.new(
            settings.SLACK_SIGNING_SECRET.encode(),
            sig_basestring.encode(),
            hashlib.sha256,
        ).hexdigest()

        response = client.post(
            "/slack/events",
            content=body,
            headers={
                "X-Slack-Request-Timestamp": timestamp,
                "X-Slack-Signature": signature,
            },
        )

        assert response.status_code == 400


class TestEventDeduplication:
    """Test event deduplication logic."""

    def test_duplicate_event_ignored(self, client, mock_slack_client):
        """Test that duplicate events with same event_id are ignored."""
        from main import event_cache

        # Clear cache before test
        event_cache.cache.clear()

        timestamp = str(int(time.time()))
        event_id = "Ev123456789"
        body = json.dumps({
            "type": "event_callback",
            "event_id": event_id,
            "event": {
                "type": "app_mention",
                "user": "U123456",
                "text": "<@UBOT> hello",
                "channel": "C123456",
                "ts": "1234567890.123456",
            },
        })

        # Create valid signature
        sig_basestring = f"v0:{timestamp}:{body}"
        from config import settings
        signature = "v0=" + hmac.new(
            settings.SLACK_SIGNING_SECRET.encode(),
            sig_basestring.encode(),
            hashlib.sha256,
        ).hexdigest()

        # Mock Slack client
        mock_slack_client.chat_postMessage.return_value = {
            "ok": True,
            "ts": "1234567890.999999"
        }
        mock_slack_client.conversations_replies.return_value = {
            "messages": [
                {"user": "U123456", "text": "<@UBOT> hello"},
            ]
        }

        # First request - should be processed
        response1 = client.post(
            "/slack/events",
            content=body,
            headers={
                "X-Slack-Request-Timestamp": timestamp,
                "X-Slack-Signature": signature,
                "Content-Type": "application/json",
            },
        )
        assert response1.status_code == 200

        # Verify event is in cache
        assert event_id in event_cache.cache

        # Second request with same event_id - should be ignored
        response2 = client.post(
            "/slack/events",
            content=body,
            headers={
                "X-Slack-Request-Timestamp": timestamp,
                "X-Slack-Signature": signature,
                "Content-Type": "application/json",
            },
        )
        assert response2.status_code == 200

        # Event should still be in cache (not duplicated)
        assert event_id in event_cache.cache

    def test_different_events_processed(self, client, mock_slack_client):
        """Test that different events with different event_ids are both processed."""
        timestamp = str(int(time.time()))

        # First event
        body1 = json.dumps({
            "type": "event_callback",
            "event_id": "Ev111111111",
            "event": {
                "type": "app_mention",
                "user": "U123456",
                "text": "<@UBOT> hello",
                "channel": "C123456",
                "ts": "1234567890.123456",
            },
        })

        # Second event with different event_id
        body2 = json.dumps({
            "type": "event_callback",
            "event_id": "Ev222222222",
            "event": {
                "type": "app_mention",
                "user": "U123456",
                "text": "<@UBOT> world",
                "channel": "C123456",
                "ts": "1234567890.234567",
            },
        })

        from config import settings
        for body in [body1, body2]:
            sig_basestring = f"v0:{timestamp}:{body}"
            signature = "v0=" + hmac.new(
                settings.SLACK_SIGNING_SECRET.encode(),
                sig_basestring.encode(),
                hashlib.sha256,
            ).hexdigest()

            mock_slack_client.chat_postMessage.return_value = {
                "ok": True,
                "ts": "1234567890.999999"
            }
            mock_slack_client.conversations_replies.return_value = {
                "messages": [
                    {"user": "U123456", "text": body},
                ]
            }

            response = client.post(
                "/slack/events",
                content=body,
                headers={
                    "X-Slack-Request-Timestamp": timestamp,
                    "X-Slack-Signature": signature,
                    "Content-Type": "application/json",
                },
            )
            assert response.status_code == 200

    def test_missing_event_id_handled(self, client, mock_slack_client):
        """Test that events without event_id are handled gracefully."""
        timestamp = str(int(time.time()))
        body = json.dumps({
            "type": "event_callback",
            # No event_id field
            "event": {
                "type": "app_mention",
                "user": "U123456",
                "text": "<@UBOT> hello",
                "channel": "C123456",
                "ts": "1234567890.123456",
            },
        })

        sig_basestring = f"v0:{timestamp}:{body}"
        from config import settings
        signature = "v0=" + hmac.new(
            settings.SLACK_SIGNING_SECRET.encode(),
            sig_basestring.encode(),
            hashlib.sha256,
        ).hexdigest()

        response = client.post(
            "/slack/events",
            content=body,
            headers={
                "X-Slack-Request-Timestamp": timestamp,
                "X-Slack-Signature": signature,
                "Content-Type": "application/json",
            },
        )

        # Should still return 200 but log error
        assert response.status_code == 200

    def test_concurrent_duplicate_events(self):
        """Test thread safety with concurrent duplicate events."""
        import threading
        from main import event_cache

        # Clear cache before test
        event_cache.cache.clear()

        event_id = "Ev_concurrent_test"
        results = []

        def check_and_mark():
            """Simulate concurrent requests with same event_id."""
            is_duplicate = event_cache.is_processed_and_mark(event_id)
            results.append(is_duplicate)

        # Create 10 threads trying to process same event simultaneously
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=check_and_mark)
            threads.append(thread)

        # Start all threads at once
        for thread in threads:
            thread.start()

        # Wait for all to complete
        for thread in threads:
            thread.join()

        # Exactly one thread should get False (newly processed)
        # All others should get True (already processed)
        assert results.count(False) == 1, f"Expected 1 False, got {results.count(False)} - Results: {results}"
        assert results.count(True) == 9, f"Expected 9 True, got {results.count(True)} - Results: {results}"

        # Event should be in cache exactly once
        assert event_id in event_cache.cache
        assert len([k for k in event_cache.cache.keys() if k == event_id]) == 1
