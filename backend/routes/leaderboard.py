from fastapi import APIRouter

router = APIRouter()

leaderboard = []

@router.post("/submit-score")
def submit_score(username: str, score: int):
    leaderboard.append({"user": username, "score": score})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    return {"leaderboard": leaderboard[:10]}

@router.get("/leaderboard")
def get_leaderboard():
    return leaderboard[:10]