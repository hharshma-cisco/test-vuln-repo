"""Flask web layer intended to break when Flask is bumped past 2.3.

The Markup helper was relocated to a sibling package in newer Flask
releases, so this module fails to import until a source edit updates
the relevant line. That is the ONLY file in the repo that exercises
the source-edit path for the agent's fix loop.
"""
from __future__ import annotations

from flask import Flask, Markup


def make_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index() -> str:
        return Markup("<b>ok</b>")

    return app
