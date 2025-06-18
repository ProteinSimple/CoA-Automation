import os
import json
from cryptography.fernet import Fernet

# KEY_PATH = os.path.expanduser("~/.yourtool/secret.key")
PUB_PATH = os.path.expanduser("~/.coat/pub.key")

# def gen_key():
#     os.makedirs(os.path.dirname(KEY_PATH), exist_ok=True)
#     key = Fernet().generate_key()
    
# def load_key():
#     if not os.path.exists(KEY_PATH):
#         gen_key()
#     with open(KEY_PATH, "w") as f:
#         return f.read()



def add_token(user: str, passkey: str):
    os.makedirs(os.path.dirname(PUB_PATH), exist_ok=True)
    with open(PUB_PATH, mode="w") as f:
        f.write(f'{user}\n{passkey}')

def load_token() -> tuple[str, str] | None:
    
    with open(PUB_PATH, mode="r") as f:
        user = f.readline().strip()
        passkey = f.readline().strip()

        return user, passkey

