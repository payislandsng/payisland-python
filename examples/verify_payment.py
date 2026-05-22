"""Verify a PayIsland transaction."""

from __future__ import annotations

import json
import os
import sys

from dotenv import load_dotenv

from payisland import PayIsland


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


if len(sys.argv) < 2:
    raise SystemExit("Usage: python examples/verify_payment.py <reference>")

load_dotenv()

payisland = PayIsland(secret_key=require_env("PAYISLAND_SECRET_KEY"))
response = payisland.transactions.verify(sys.argv[1])

print(json.dumps(response, indent=2))
