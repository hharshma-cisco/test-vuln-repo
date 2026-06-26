"""Tests for app.py — these run after every dependency bump."""
import os
import tempfile

import pytest

from app import add, greet, encrypt_message, decrypt_message, load_config, generate_rsa_key


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_greet():
    assert greet("world") == "Hello, world!"
    assert greet("Alice") == "Hello, Alice!"


def test_encrypt_decrypt_roundtrip():
    key, token = encrypt_message("secret data")
    result = decrypt_message(key, token)
    assert result == "secret data"


def test_encrypt_returns_bytes():
    key, token = encrypt_message("hello")
    assert isinstance(key, bytes)
    assert isinstance(token, bytes)


def test_generate_rsa_key():
    key = generate_rsa_key()
    assert key.key_size == 2048


def test_load_config():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("app:\n  name: test\n  version: 1\n")
        tmp = f.name
    try:
        config = load_config(tmp)
        assert config["app"]["name"] == "test"
        assert config["app"]["version"] == 1
    finally:
        os.unlink(tmp)
