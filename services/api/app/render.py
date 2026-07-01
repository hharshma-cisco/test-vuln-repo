"""Templating helpers built on jinja2.

API used (`Template.render`) is unchanged across the bumped jinja2 version,
so tests pass without source edits.
"""
from __future__ import annotations

from jinja2 import Template


def render_greeting(name: str) -> str:
    tmpl = Template("hello, {{ name }}!")
    return tmpl.render(name=name)
