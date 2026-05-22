"""Transaction API resource."""

from __future__ import annotations

from typing import Any

from payisland.support.http_client import HttpClient


class TransactionsResource:
    """Transaction operations for inbound PayIsland payments."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def initialize(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Initialize an inbound transaction."""
        if not isinstance(payload, dict):
            raise TypeError("payload must be a dictionary")

        return self._http_client.post(
            "/api/v1/transactions/in/initialize",
            json=payload,
        )

    def verify(self, reference: str) -> dict[str, Any]:
        """Verify an inbound transaction by reference."""
        if not isinstance(reference, str) or not reference.strip():
            raise ValueError("reference is required")

        return self._http_client.get(
            f"/api/v1/transactions/in/check-transaction-status/{reference}"
        )
