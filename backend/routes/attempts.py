from fastapi import APIRouter
from pydantic import BaseModel
from db import attempts_collection

router = APIRouter()

class Attempt(BaseModel):
    user: str
    question: str
    score: int

@router.post("/")
def save_attempt(data: Attempt):
    attempts_collection.insert_one(data.dict())
    return {"message": "saved"}