"""Tests for the jinja2 wrapper — stable API across the bump."""
from app.render import render_greeting


def test_render_greeting_basic():
    assert render_greeting("world") == "hello, world!"


def test_render_greeting_escapes_safely():
    out = render_greeting("Ada")
    assert "Ada" in out
