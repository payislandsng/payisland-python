from __future__ import annotations

import hmac
from hashlib import sha256

from payisland import PayIsland


def test_valid_webhook_signature_returns_true() -> None:
    payisland = PayIsland(secret_key="test_xxx")
    payload = '{"transaction_reference":"order_12345"}'
    secret = "webhook_secret"
    signature = hmac.new(secret.encode(), payload.encode(), sha256).hexdigest()

    assert payisland.webhooks.verify_signature(payload, signature, secret) is True


def test_valid_webhook_signature_with_prefix_returns_true() -> None:
    payisland = PayIsland(secret_key="test_xxx")
    payload = b'{"transaction_reference":"order_12345"}'
    secret = "webhook_secret"
    signature = hmac.new(secret.encode(), payload, sha256).hexdigest()

    assert (
        payisland.webhooks.verify_signature(payload, f"sha256={signature}", secret)
        is True
    )


def test_invalid_webhook_signature_returns_false() -> None:
    payisland = PayIsland(secret_key="test_xxx")

    assert (
        payisland.webhooks.verify_signature(
            payload='{"transaction_reference":"order_12345"}',
            signature="invalid",
            secret="webhook_secret",
        )
        is False
    )


def test_mismatched_or_empty_signature_returns_false() -> None:
    payisland = PayIsland(secret_key="test_xxx")

    assert payisland.webhooks.verify_signature("payload", "", "webhook_secret") is False
    assert (
        payisland.webhooks.verify_signature("payload", "mismatched", "webhook_secret")
        is False
    )
