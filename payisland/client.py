"""PayIsland SDK client."""

from __future__ import annotations

from payisland.resources.transactions import TransactionsResource
from payisland.resources.webhooks import WebhooksResource
from payisland.support.http_client import HttpClient


class PayIsland:
    """Main entrypoint for PayIsland API integrations."""

    DEFAULT_BASE_URL = "https://ags.payislands.com"

    def __init__(
        self,
        secret_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int | float = 30,
    ) -> None:
        if not isinstance(secret_key, str) or not secret_key.strip():
            raise ValueError("secret_key is required")

        self.secret_key = secret_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self._http_client = HttpClient(
            secret_key=self.secret_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )
        self.transactions = TransactionsResource(self._http_client)
        self.webhooks = WebhooksResource()
