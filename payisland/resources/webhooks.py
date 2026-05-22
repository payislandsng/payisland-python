"""Webhook helpers."""

from __future__ import annotations

import hmac
from hashlib import sha256


class WebhooksResource:
    """Webhook verification helpers."""

    def verify_signature(
        self,
        payload: str | bytes,
        signature: str,
        secret: str,
    ) -> bool:
        """Verify a webhook signature using HMAC SHA256."""
        if not signature or not secret:
            return False

        if isinstance(payload, str):
            payload_bytes = payload.encode("utf-8")
        elif isinstance(payload, bytes):
            payload_bytes = payload
        else:
            return False

        normalized_signature = signature.strip()
        if normalized_signature.startswith("sha256="):
            normalized_signature = normalized_signature.removeprefix("sha256=")

        if not normalized_signature:
            return False

        expected_signature = hmac.new(
            secret.encode("utf-8"),
            payload_bytes,
            sha256,
        ).hexdigest()

        return hmac.compare_digest(expected_signature, normalized_signature)
