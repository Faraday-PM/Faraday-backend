import sqlalchemy.exc
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.util.common import load_config
from cryptography.hazmat.primitives import constant_time
from fastapi import HTTPException
import base64
from Crypto.Random import get_random_bytes

config: dict = load_config()

# Must be at top of file before classes or anything is loaded
# Prevent some error, I forget
Base = declarative_base()


class Salt(Base):
    __tablename__ = "salts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, ForeignKey("users.username"), unique=True)
    salt = Column(String, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


class Vault(Base):
    __tablename__ = "vaults"
    id = Column(Integer, primary_key=True, autoincrement=True)
    master = Column(String, ForeignKey("users.username"), unique=True)
    vault = Column(String)
    iv = Column(String)


# Probably not a good idea to load more than one instance of DatabaseHandler
class DatabaseHandler:
    @staticmethod
    def _create_salt(salt: bytes, username: str) -> bool:
        try:
            salt: Salt = Salt(username=username, salt=salt)
            session.rollback()
            session.add(salt)
            session.commit()
            return True
        except sqlalchemy.exec.IntegrityError:
            return False
    
    @staticmethod
    def get_salt(username: str) -> bytes:
        cursor = session.query(Salt).filter(Salt.username == username)
        for salt in cursor:
            return salt.salt

    @staticmethod
    def create_user(username: str, password: str, salt: bytes) -> str:
        try:
            user: User = User(username=username, password=password)
            session.rollback()
            session.add(user)
            session.commit()
            s = DatabaseHandler._create_salt(salt, username)
            if s is None:
                raise HTTPException(status_code=500, detail="Unable to create salt")
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=400, detail="User already exists")
        return "Added User Successfully!"

    @staticmethod
    def login(username: str, password: str) -> str:
        try:
            cursor = session.query(User).filter(User.username == username)
            for user in cursor:
                db_password = user.password
                # print(db_password)
            # This function helps prevent against timing attacks, O(n)
            # Attacker does not know how long the data is, or how long it takes to perform the operation
            # Read more: https://codahale.com/a-lesson-in-timing-attacks/
                if constant_time.bytes_eq(password.encode(config["format"]), user.password.encode(config["format"])):
                    # The reference of db_password suggests UnBoundLocalError, this is fine it is how we detect no account
                    return "Successfully authenticated!"
            raise HTTPException(
                status_code=400, detail="Incorrect username or password")
        except UnboundLocalError:       # No user found
            raise HTTPException(
                status_code=400, detail="Incorrect username or password")

    @staticmethod
    def get_iv(username):
        cursor = session.query(Vault).filter(Vault.master == username)
        for vault in cursor:
            return str(vault.iv)

    @staticmethod
    def get_vault(username):
        cursor = session.query(Vault).filter(Vault.master == username)
        for vault in cursor:
            return vault.vault

    @staticmethod
    def create_vault(master: str, vault: str = base64.b64encode("{}".encode(config["format"]))):
        v = Vault(master=master, vault=vault, iv=get_random_bytes(16).hex())
        session.rollback()
        session.add(v)
        session.commit()

    @staticmethod
    def update_vault(username, new_vault):
        session.query(Vault).filter(Vault.master == username).update(
            {Vault.vault: new_vault})
        session.commit()


# Sqlalchemy boilerplate
# Generating sqlalchemy stuff
print(config["DATABASE_URL"])
engine = create_engine(config["DATABASE_URL"], echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
