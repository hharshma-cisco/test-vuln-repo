"""Tests for the requests/urllib3 helpers — no network."""
from app.http_client import build_retry


def test_build_retry_default_total():
    r = build_retry()
    assert r.total == 3


def test_build_retry_custom_total():
    r = build_retry(total=7)
    assert r.total == 7


def test_fetch_status_callable():
    from app.http_client import fetch_status
    assert callable(fetch_status)
