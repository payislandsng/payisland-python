"""Initialize a PayIsland card transaction."""

from __future__ import annotations

import os

from dotenv import load_dotenv

from payisland import PayIsland


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


load_dotenv()

secret_key = require_env("PAYISLAND_SECRET_KEY")
payment_item_id = require_env("PAYISLAND_PAYMENT_ITEM_ID")

payisland = PayIsland(secret_key=secret_key)

response = payisland.transactions.initialize(
    {
        "callback_url": "https://example.com/webhooks/payislands",
        "payment_item_id": payment_item_id,
        "transaction_reference": "order_12345",
        "channel": "card",
        "amount": "1000",
        "customer_info": {
            "email": "ada@example.com",
            "phone_number": "08011112222",
            "first_name": "Ada",
            "last_name": "Lovelace",
        },
    }
)

authorization_url = response.get("data", {}).get("authorization_url")
print(authorization_url if authorization_url else response)
