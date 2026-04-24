from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import hashlib
import time
import random

router = APIRouter()

# =========================
# 📦 MODELS
# =========================
class User(BaseModel):
    username: str
    password: str

class Attempt(BaseModel):
    username: str
    question: str
    score: int
    code: str

# =========================
# 🧠 FAKE DATABASE (replace later with MongoDB/Postgres)
# =========================
users_db = {}
attempts_db = []

# =========================
# 🔐 AUTH SYSTEM
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/auth/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    users_db[user.username] = hash_password(user.password)
    return {"message": "User registered successfully"}

@router.post("/auth/login")
def login(user: User):
    if user.username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    if users_db[user.username] != hash_password(user.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    return {"message": "Login successful", "username": user.username}


# =========================
# 📝 SAVE ATTEMPT
# =========================
@router.post("/attempts/save")
def save_attempt(data: Attempt):
    attempts_db.append({
        "username": data.username,
        "question": data.question,
        "score": data.score,
        "code": data.code,
        "timestamp": time.time()
    })

    return {"message": "Attempt saved"}


# =========================
# 📊 USER HISTORY
# =========================
@router.get("/attempts/{username}")
def get_attempts(username: str):
    user_attempts = [a for a in attempts_db if a["username"] == username]
    return user_attempts


# =========================
# 🏆 LEADERBOARD
# =========================
@router.get("/leaderboard")
def leaderboard():
    scores = {}

    for a in attempts_db:
        user = a["username"]
        scores[user] = scores.get(user, 0) + a["score"]

    sorted_users = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return [{"username": u, "score": s} for u, s in sorted_users]


# =========================
# 🧠 HUGE QUESTION SYSTEM (SIMULATED)
# =========================
# (Later replace with DB or API like LeetCode dataset)

questions_big = {
    "easy": [
        {"title": "Palindrome Check", "description": "Check if string is palindrome"},
        {"title": "Reverse String", "description": "Reverse a string"},
        {"title": "Factorial", "description": "Calculate factorial"}
    ] * 50,  # simulate 150 questions

    "medium": [
        {"title": "Two Sum", "description": "Find pair with sum"},
        {"title": "Longest Substring", "description": "Without repeating chars"},
    ] * 50,

    "hard": [
        {"title": "LRU Cache", "description": "Design cache"},
        {"title": "Median Arrays", "description": "Median of arrays"},
    ] * 50
}

@router.get("/questions/{difficulty}")
def get_questions(difficulty: str):

  return random.choice(questions_big.get(difficulty, []))


# =========================
# 🕵️ PLAGIARISM CHECK
# =========================
def similarity(a, b):
    return len(set(a.split()) & set(b.split())) / max(len(a.split()), 1)

@router.post("/plagiarism")
def check_plagiarism(code: str):
    for attempt in attempts_db:
        sim = similarity(code, attempt["code"])
        if sim > 0.8:
            return {
                "plagiarism": True,
                "matched_user": attempt["username"],
                "similarity": round(sim, 2)
            }

    return {"plagiarism": False}