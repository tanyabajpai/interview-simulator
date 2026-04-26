from fastapi import APIRouter
from services.db import attempts_collection

router = APIRouter()


@router.get("/leaderboard")
def get_leaderboard():
    pipeline = [
        {
            "$group": {
                "_id": "$username",
                "score": {"$avg": "$score"}   # average score
            }
        },
        {
            "$sort": {"score": -1}
        },
        {
            "$limit": 10
        }
    ]

    results = list(attempts_collection.aggregate(pipeline))

    leaderboard = [
        {
            "username": r["_id"],
            "score": int(r["score"])
        }
        for r in results
    ]

    return leaderboard