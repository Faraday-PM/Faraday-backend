from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json
import requests as r
import hashlib

schema = {
    'vault': [
        {
            'url': 'https://google.com',
            'username': 'richardjackson@yahoo.com',
            'password': '!5bAcX&VuK'
        },
        {
            'url': 'https://youtube.com',
            'username': 'iwilson@hotmail.com',
            'password': '+4CrUi5%*t'
        },
        {
            'url': 'https://facebook.com',
            'username': 'hmcgee@hotmail.com',
            'password': 'Y*kp9XKVCd'
        },
        {
            'url': 'https://instagram.com',
            'username': 'isantiago@yahoo.com',
            'password': 'h%an0YveZ#'
        },
        {
            'url': 'https://twitter.com',
            'username': 'brian68@gmail.com',
            'password': '@qO@LwZ(M2'
        }
    ]
}

url = "http://127.0.0.1:8000"
salt = b"salt"  # b"4841cd0e0fd6e41b56d9fa6b3d50d47b6e6504d69e1528f78b627f4f8974d0f1588586e18e4e7bc6fcebaf52a546f6c43828c8468b8181d32e69c461ef7182112008bfff44650957f508ff2bd4ee58912d442e7e7f73471fdc09edc03cde2b0ff4336ef2f270139bd1426906248c5dd4bb965cb5632bb78d36c4114213f645ebcfce7d9f33065f116f6b7a173a42093f2923e15081438bdd19f4693ae1e6c1a768b05dd8a49dfe27fa98f1b460108de65aae4f98f5896a5606429e178d8b751fffa2f34f320638e6fb30e519a80da5fc088b8c91a9b766d08f26d486dc11b74d54c0652f6ac2c1813a3f945d4e69a4db51d286b12b00a65e9a26ba3472c0b369"
username = "testing123"
unhashed_password = f"{username}password123"
password = hashlib.pbkdf2_hmac(
    "sha256", unhashed_password.encode('utf-8'), salt, 600_000).hex()
print(password)


def register():
    body = {
        "username": "testing123",
        "password": password
    }
    res = r.post(f'{url}/register', json=body)
    print(res.json())

# register()


def getiv():
    body = {
        "username": "testing123",
        "password": password
    }
    res = r.post(f"{url}/iv", json=body)
    server_iv: str = res.json()["iv"]
    return bytes.fromhex(server_iv)


def encrypt_vault() -> str:
    """
        # Long version


        obj = AES.new(key, AES.MODE_CBC, iv)
        message = str(schema).encode("utf-8")

        ciphertext = obj.encrypt(pad(message, AES.block_size))

        hexformat = ciphertext.hex()

        return hexformat
    """

    # Condensed version
    key = hashlib.pbkdf2_hmac(
        "sha256", b"password123", salt, 600_000, dklen=32)
    iv = getiv()

    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(str(schema).encode("utf-8"), AES.block_size)).hex()


def updateVault():
    body = {
        "username": "testing123",
        "password": password,
        "vault": encrypt_vault()
    }

    res = r.post(f"{url}/vault", json=body)

    print(res.json())


def getVault():
    key = hashlib.pbkdf2_hmac(
        "sha256", b"password123", salt, 600_000, dklen=32)
    iv = getiv()

    body = {
        "username": "testing123",
        "password": password,
    }
    res = r.post(f"{url}/auth", json=body)

    print(f"Recieved from server: {res.json()}")

    # Condensed version
    print(json.loads(unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(bytes.fromhex(
        res.json()["vault"])), AES.block_size).decode().replace("'", '"')))

    """
    # Long version 
    # transform hex into dict
    vault = res.json()["vault"]
    bytes_vault = bytes.fromhex(vault)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Replace ' with " because of quirk in json.loads
    # json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
    plaintext = unpad(cipher.decrypt(bytes_vault), AES.block_size).decode("utf-8").replace("'", '"')

    json_vault = json.loads(plaintext)

    print(json_vault)
    """


mode = input("Encrypt or Decrypt or register (e/d/r): ")
if mode == "e":
    updateVault()
elif mode == "d":
    getVault()
elif mode == "r":
    register()
"""
key = hashlib.pbkdf2_hmac("sha256", b"password123", salt, 600_000, dklen=32)
iv = getiv()


obj = AES.new(key, AES.MODE_CBC, iv)
message = str(schema).encode("utf-8")

ciphertext = obj.encrypt(pad(message, AES.block_size))

print(ciphertext)

obj2 = AES.new(key, AES.MODE_CBC, iv)

# Replace ' with " cause of quirk with json.loads
plaintext = unpad(obj2.decrypt(ciphertext), AES.block_size).decode().replace("'", '"')

json_data = json.loads(plaintext)


print(json_data)"""
