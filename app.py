"""Tiny app that uses a few packages — kept simple so the bump doesn't break anything."""


def add(a: int, b: int) -> int:
    return a + b


def greet(name: str) -> str:
    return f"hello, {name}"
