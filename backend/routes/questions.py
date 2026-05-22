from fastapi import APIRouter
from services.question_bank import get_random_question

router = APIRouter()


@router.get("/{difficulty}")
def get_question(difficulty: str):
    """
    Returns a single randomly selected question for the given difficulty.
    Frontend receives: { title, description, ... }
    """
    return get_random_question(difficulty)