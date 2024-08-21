import os
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()

"""# Skips having to rewrite the same code in nearly every file
def load_config() -> dict:
    with open(os.path.join(os.getcwd(), "config.faraday.json")) as f:
        data: dict = json.load(f)
    return data
"""


class config_type(TypedDict):
    hash_name: str
    DATABASE_URL: str
    format: str
    allowConns: bool
    email: bool


def load_config() -> config_type:
    return {
        "hash_name": "sha256",
        "DATABASE_URL": os.environ["FARADAY_DATABASE_URL"],
        "format": "utf-8",
        "allowConns": True,
        "email": False
    }
