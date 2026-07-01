"""HTTP helpers built on requests + urllib3.

Public API is stable across the versions the agent will bump to. Tests
pass without any source edit — this is a "safe bump" path.
"""
from __future__ import annotations

import requests
from urllib3.util.retry import Retry


def build_retry(total: int = 3) -> Retry:
    return Retry(total=total, backoff_factor=0.1)


def fetch_status(url: str, timeout: float = 5.0) -> int:
    resp = requests.get(url, timeout=timeout)
    return resp.status_code
