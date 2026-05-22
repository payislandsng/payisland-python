"""Verify a PayIsland webhook signature."""

from __future__ import annotations

import os

from dotenv import load_dotenv

from payisland import PayIsland

load_dotenv()

payisland = PayIsland(secret_key=os.getenv("PAYISLAND_SECRET_KEY", "test_key"))

raw_payload = b'{"transaction_reference":"order_12345","status":"successful"}'
signature = "signature-from-payisland-webhook-header"
webhook_secret = os.getenv("PAYISLAND_WEBHOOK_SECRET", "your_webhook_secret")

is_valid = payisland.webhooks.verify_signature(
    payload=raw_payload,
    signature=signature,
    secret=webhook_secret,
)

print(f"Webhook signature valid: {is_valid}")
print(
    "Verify the webhook signature and confirm the transaction reference with "
    "PayIsland before fulfillment."
)
