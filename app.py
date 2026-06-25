"""Fake app — uses deliberately old dependency versions for testing the agent."""
import requests
import yaml
from cryptography.fernet import Fernet


def fetch_data(url: str) -> dict:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def encrypt_message(message: str) -> tuple:
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(message.encode())
    return key, token


def decrypt_message(key: bytes, token: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(token).decode()


def add(a: int, b: int) -> int:
    return a + b


def greet(name: str) -> str:
    return f"Hello, {name}!"
