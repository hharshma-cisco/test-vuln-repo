from app.http_client import build_retry


def test_build_retry_defaults():
    r = build_retry()
    assert r.total == 3


def test_build_retry_custom():
    r = build_retry(total=5)
    assert r.total == 5
