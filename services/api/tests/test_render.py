from app.render import render_greeting


def test_render_greeting():
    assert render_greeting("world") == "hello, world!"
