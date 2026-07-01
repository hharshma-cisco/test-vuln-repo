"""services/api — small Flask + requests app used to exercise the agent.

`from app import add, greet` — importing these functions requires the
package to be importable at all. The Flask import in `web.py` will BREAK
after the bump; that's the whole point.
"""


def add(a: int, b: int) -> int:
    return a + b


def greet(name: str) -> str:
    return f"hello, {name}"
