"""HTTP support for the PayIsland SDK."""

from __future__ import annotations

from typing import Any

import requests

from payisland.exceptions import PayIslandAPIError


class HttpClient:
    """Small requests-based HTTP client for PayIsland API calls."""

    def __init__(
        self,
        secret_key: str,
        base_url: str,
        timeout: int | float,
    ) -> None:
        self.secret_key = secret_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "payisland-python",
        }

    def get(self, path: str) -> dict[str, Any]:
        return self._request("GET", path)

    def post(self, path: str, json: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", path, json=json)

    def _request(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json,
                headers=self.headers,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise PayIslandAPIError(str(exc)) from exc

        response_data = self._parse_response(response)

        if response.status_code >= 400:
            raise PayIslandAPIError(
                message=self._error_message(response, response_data),
                status_code=response.status_code,
                response_data=response_data,
            )

        return response_data

    def _parse_response(self, response: requests.Response) -> dict[str, Any]:
        if not response.content:
            return {}

        try:
            data = response.json()
        except ValueError:
            return {"raw": response.text}

        if isinstance(data, dict):
            return data

        return {"data": data}

    def _error_message(
        self,
        response: requests.Response,
        response_data: dict[str, Any],
    ) -> str:
        for key in ("message", "error"):
            value = response_data.get(key)
            if isinstance(value, str) and value:
                return value

        if response.text:
            return response.text

        return f"PayIsland API request failed with status {response.status_code}"
