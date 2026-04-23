from fastapi import APIRouter

router = APIRouter()

users = {}

@router.post("/login")
def login(username: str):
    users[username] = {"score": 0}
    return {"message": "Logged in", "user": username}