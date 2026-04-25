from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from services.db import users_collection, attempts_collection
from services.auth_service import hash_password, verify_password, create_access_token
from services.deps import get_current_user

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from services.deps import get_current_user

router = APIRouter()


# =========================
# MODELS
# =========================
class UserSignup(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# =========================
# SIGNUP
# =========================
@router.post("/signup")
def signup(data: UserSignup):
    if users_collection.find_one({"username": data.username}):
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(data.password)

    users_collection.insert_one({
        "username": data.username,
        "password": hashed
    })

    return {"message": "User created successfully"}


# =========================
# LOGIN
# =========================
@router.post("/login")
def login(data: UserLogin):
    user = users_collection.find_one({"username": data.username})

    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"username": data.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# 🔐 SAVE ATTEMPT (PROTECTED)
# =========================

@router.post("/save")
def save_attempt(data: dict, username: str = Depends(get_current_user)):
    data["username"] = username
    data["timestamp"] = datetime.utcnow()

    attempts_collection.insert_one(data)
    return {"message": "Saved"}

# =========================
# 📊 USER STATS (PROTECTED)
# =========================
@router.get("/stats")
def get_stats(username: str = Depends(get_current_user)):
    attempts = list(attempts_collection.find({"username": username}))

    total = len(attempts)

    if total == 0:
        return {
            "total_attempts": 0,
            "avg_score": 0
        }

    avg = sum(a.get("score", 0) for a in attempts) // total

    return {
        "total_attempts": total,
        "avg_score": avg
    }