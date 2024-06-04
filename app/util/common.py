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
    salt: str
    format: str


def load_config() -> config_type:
    return {
        "hash_name": "sha256",
        "DATABASE_URL": os.environ["FARADAY_DATABASE_URL"],
        "salt": "4841cd0e0fd6e41b56d9fa6b3d50d47b6e6504d69e1528f78b627f4f8974d0f1588586e18e4e7bc6fcebaf52a546f6c43828c8468b8181d32e69c461ef7182112008bfff44650957f508ff2bd4ee58912d442e7e7f73471fdc09edc03cde2b0ff4336ef2f270139bd1426906248c5dd4bb965cb5632bb78d36c4114213f645ebcfce7d9f33065f116f6b7a173a42093f2923e15081438bdd19f4693ae1e6c1a768b05dd8a49dfe27fa98f1b460108de65aae4f98f5896a5606429e178d8b751fffa2f34f320638e6fb30e519a80da5fc088b8c91a9b766d08f26d486dc11b74d54c0652f6ac2c1813a3f945d4e69a4db51d286b12b00a65e9a26ba3472c0b369",
        "format": "utf-8"
    }
