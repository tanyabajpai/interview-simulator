from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FIX: os.getenv(VAR_NAME, fallback) — first arg is the env var NAME, not value
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret123")
ALGORITHM = "HS256"


def hash_password(password: str):
    password = password[:72]  # prevent bcrypt 72-byte crash
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str):
    plain = plain[:72]
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)