from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class VaultUpdate(User):
    vault: str