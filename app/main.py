from app.util.keyderivation import derive_auth_key
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import app.db_interaction as db_interaction
from app.util.common import load_config
from typing import Annotated
from app.models import User, VaultUpdate
import requests
import base64
import grab_favicon as gf
from dotenv import load_dotenv

load_dotenv()

db: db_interaction.DatabaseHandler = db_interaction.DatabaseHandler()

config: dict = load_config()

app: FastAPI = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get('/')
async def root():
    return {"msg": "message"}


@app.post("/register")
async def register(user: User):
    hashed_password = derive_auth_key(
        user.password, config["salt"].encode(config["format"]))
    res = db.create_user(user.username, hashed_password)
    db.create_vault(user.username)
    return {"msg": res}


# Get vault
@app.post("/auth")
async def login(user: User):
    hashed_password = derive_auth_key(
        user.password, config["salt"].encode(config["format"]))
    res: str = db.login(user.username, hashed_password)

    base64_vault: str = db.get_vault(user.username)
    return {
        "msg": res,
        "vault": base64_vault
    }


# Update vault
@app.post("/vault")
async def update_vault(user: VaultUpdate):
    hashed_password = derive_auth_key(
        user.password, config["salt"].encode(config["format"]))
    res: str = db.login(user.username, hashed_password)
    db.update_vault(user.username, user.vault)
    return {"msg": res}


@app.get("/favicon")
async def get_favicon(url: str):
    url = url.replace("http://", "").replace("https://", "")
    try:
        print(url)
        with open(f"util/favicons/{url}.png", "rb") as img_file:
            encodedIcon = base64.b64encode(img_file.read())
    except FileNotFoundError as e:
        gf.download_favicon(url, "util/favicons")
        with open(f"util/favicons/{url}.png", "rb") as img_file:
            encodedIcon = base64.b64encode(img_file.read())
    return {"msg": encodedIcon}


# Hopefully protected and no security flaws
@app.post("/iv")
async def getIv(user: User):
    hashed_password = derive_auth_key(
        user.password, config["salt"].encode(config["format"]))
    res: str = db.login(user.username, hashed_password)
    if res == "Successfully authenticated!":
        iv = db.get_iv(user.username)
        return {"msg": res, "iv": iv}
    else:
        return {"msg": "User not found"}
