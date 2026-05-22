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