from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("supersecret123", "fallbacksecret")
ALGORITHM = "HS256"


# =========================
# 🔐 SAFE PASSWORD HASHING
# =========================
def hash_password(password: str):
    password = password[:72]  # 🔥 FIX: prevent bcrypt crash
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str):
    plain = plain[:72]  # 🔥 FIX
    return pwd_context.verify(plain, hashed)


# =========================
# 🎫 TOKEN GENERATION
# =========================
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)