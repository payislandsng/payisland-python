# PayIsland Python SDK

![CI](https://github.com/payislandsng/payisland-python/actions/workflows/ci.yml/badge.svg)

Official Python SDK for integrating with PayIsland payment APIs.

## Installation

```bash
pip install payisland
```

## Initialization

```python
from payisland import PayIsland

payisland = PayIsland(secret_key="test_xxx")
```

The SDK uses `https://ags.payislands.com` by default. Sandbox or live mode is
determined by the API key you provide; there is no separate environment flag in
the SDK.

## Transaction Initialization

```python
from payisland import PayIsland

payisland = PayIsland(secret_key="test_xxx")

response = payisland.transactions.initialize(
    {
        "callback_url": "https://example.com/webhooks/payislands",
        "payment_item_id": "6",
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

print(response["data"]["authorization_url"])
```

For card transactions, the customer may need to complete 3DS authentication
after initialization. Treat the transaction as pending until you verify the
transaction reference and receive a successful final status from PayIsland.

## Transaction Verification

```python
response = payisland.transactions.verify("order_12345")
print(response)
```

This calls:

```text
GET /api/v1/transactions/in/check-transaction-status/{reference}
```

## Webhook Verification

```python
is_valid = payisland.webhooks.verify_signature(
    payload=raw_payload,
    signature=signature,
    secret=webhook_secret,
)
```

Webhook signatures are verified using HMAC SHA256 and constant-time comparison.
Always verify the webhook signature and verify the transaction reference before
fulfilling an order.

## Error Handling

API errors raise `PayIslandAPIError` and include the status code and response
body when available.

```python
from payisland import PayIsland, PayIslandAPIError

payisland = PayIsland(secret_key="test_xxx")

try:
    response = payisland.transactions.verify("order_12345")
except PayIslandAPIError as exc:
    print(exc.message)
    print(exc.status_code)
    print(exc.response_data)
```

## Development

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
python -m build
twine check dist/*
```

## License

MIT
