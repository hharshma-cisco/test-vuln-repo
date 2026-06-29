"""Tests for the Flask web layer.

These tests FAIL after the agent bumps Flask past 2.3 because the source code
in app/web.py still does `from flask import Markup` — which no longer exists.

This is intentional: it forces the agent to run analyze_failure → edit_code
and verifies that the LLM-driven source edit path works end-to-end.
"""
import importlib.metadata
import werkzeug

# Werkzeug 3.x removed __version__ attribute; add it back for compatibility
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = importlib.metadata.version('werkzeug')

from app.web import make_app


def test_index_returns_ok():
    app = make_app()
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"ok" in resp.data
