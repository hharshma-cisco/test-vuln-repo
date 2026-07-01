"""Flask web layer — INTENTIONALLY FRAGILE.

`Markup` was removed from Flask in 2.3 (moved to `markupsafe`). When the
agent bumps Flask past 2.3, this import breaks and every test that
touches `make_app()` fails at collection time. That kicks the agent into
`analyze_failure → edit_code → run_tests` — the LLM must produce:

    from flask import Flask, Markup    →    from flask import Flask
                                             from markupsafe import Markup

This is the ONLY file in the repo that exercises the LLM edit path.
"""
from __future__ import annotations

from flask import Flask, Markup


def make_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index() -> str:
        return Markup("<b>ok</b>")

    return app
