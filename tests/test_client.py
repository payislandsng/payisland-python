from __future__ import annotations

import pytest

from payisland import PayIsland


def test_client_requires_secret_key() -> None:
    with pytest.raises(ValueError, match="secret_key is required"):
        PayIsland(secret_key="")


def test_default_base_url() -> None:
    payisland = PayIsland(secret_key="test_xxx")

    assert payisland.base_url == "https://ags.payislands.com"


def test_custom_base_url_override() -> None:
    payisland = PayIsland(
        secret_key="test_xxx",
        base_url="https://example.test/",
    )

    assert payisland.base_url == "https://example.test"
