import os

from cryptography.fernet import Fernet

PUB_PATH = os.path.expanduser("~/.coat/pub.key")
FERNET_KEY = b"Xh4RzRkR1BlOxsib-EeVjFQZ-WTwvvbr3SK0oZmQ3lo="


fernet = Fernet(FERNET_KEY)


def add_token(user: str, passkey: str):
    os.makedirs(os.path.dirname(PUB_PATH), exist_ok=True)
    content = f"{user}\n{passkey}".encode("utf-8")
    encrypted = fernet.encrypt(content)
    with open(PUB_PATH, "wb") as f:
        f.write(encrypted)


def load_token() -> tuple[str, str] | None:
    try:
        with open(PUB_PATH, "rb") as f:
            enc = f.read()
        content = fernet.decrypt(enc).decode("utf-8")
        user, passkey = content.strip().split("\n", 1)
        return user, passkey
    except Exception as e:
        print(f"Failed to load token: {e}")
        return None
