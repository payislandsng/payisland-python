from __future__ import annotations

import pytest
import responses

from payisland import PayIsland
from payisland.exceptions import PayIslandAPIError


def test_transactions_initialize_sends_post() -> None:
    payisland = PayIsland(secret_key="test_xxx")
    url = "https://ags.payislands.com/api/v1/transactions/in/initialize"

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.POST,
            url,
            json={"status": True, "data": {"authorization_url": "https://pay.test"}},
            status=200,
        )

        response = payisland.transactions.initialize(
            {
                "callback_url": "https://example.com/webhooks/payislands",
                "payment_item_id": "6",
                "transaction_reference": "order_12345",
                "channel": "card",
                "amount": "1000",
                "customer_info": {"email": "ada@example.com"},
            }
        )

        request = rsps.calls[0].request

    assert request.method == "POST"
    assert request.url == url
    assert request.headers["Authorization"] == "Bearer test_xxx"
    assert request.headers["Content-Type"] == "application/json"
    assert request.headers["Accept"] == "application/json"
    assert request.headers["User-Agent"] == "payisland-python"
    assert response["data"]["authorization_url"] == "https://pay.test"


def test_transactions_verify_sends_get() -> None:
    payisland = PayIsland(secret_key="test_xxx")
    reference = "order_12345"
    url = (
        "https://ags.payislands.com/api/v1/transactions/in/"
        f"check-transaction-status/{reference}"
    )

    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            url,
            json={"status": True, "data": {"transaction_reference": reference}},
            status=200,
        )

        response = payisland.transactions.verify(reference)

        request = rsps.calls[0].request

    assert request.method == "GET"
    assert request.url == url
    assert response["data"]["transaction_reference"] == reference


def test_api_error_response_raises_payisland_api_error() -> None:
    payisland = PayIsland(secret_key="test_xxx")
    url = "https://ags.payislands.com/api/v1/transactions/in/initialize"
    response_data = {"message": "Invalid payment item", "code": "bad_request"}

    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, url, json=response_data, status=400)

        with pytest.raises(PayIslandAPIError) as exc_info:
            payisland.transactions.initialize({"payment_item_id": "bad"})

    error = exc_info.value
    assert error.status_code == 400
    assert error.response_data == response_data
    assert error.message == "Invalid payment item"
