from fastapi import APIRouter
from services.question_bank import get_random_question

router = APIRouter()

@router.get("/{difficulty}")
def get_question(difficulty: str):
    return get_random_question(difficulty)