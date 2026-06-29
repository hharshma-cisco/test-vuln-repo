"""Flask web layer.

This module is intentionally fragile: it imports `Markup` from `flask`, which
was REMOVED in Flask 2.3 (moved to `markupsafe`). When the agent bumps Flask,
the import will break and the LLM-driven source-edit path will need to:

    from flask import Flask, Markup     →     from flask import Flask
                                              from markupsafe import Markup

This is the only file in the repo that exercises the analyze_failure → edit_code
loop. The other modules give the agent easy wins so we can see the full DAG run.
"""
from __future__ import annotations

from flask import Flask, Markup


def make_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index() -> str:
        return Markup("<b>ok</b>")

    return app
