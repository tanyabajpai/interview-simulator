from fastapi import APIRouter
from services.db import users_collection

router = APIRouter()

@router.get("/leaderboard")
def get_leaderboard():
    users = list(
        users_collection.find({}, {"_id": 0, "username": 1, "best_score": 1})
        .sort("best_score", -1)
        .limit(10)
    )

    return {"leaderboard": users}