from fastapi import APIRouter
from pydantic import BaseModel
from db import attempts_collection

from fastapi import APIRouter, Depends
from services.db import attempts_collection
from services.deps import get_current_user

router = APIRouter()

@router.get("/history")
def get_history(username: str = Depends(get_current_user)):
    attempts = list(
        attempts_collection.find({"username": username})
        .sort("timestamp", -1)
        .limit(10)
    )

    for a in attempts:
        a["_id"] = str(a["_id"])

    return attempts

router = APIRouter()

class Attempt(BaseModel):
    user: str
    question: str
    score: int

@router.post("/")
def save_attempt(data: Attempt):
    attempts_collection.insert_one(data.dict())
    return {"message": "saved"}