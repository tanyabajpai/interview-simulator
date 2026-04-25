from pydantic import BaseModel
from typing import List, Dict


class Attempt(BaseModel):
    question: str
    score: int
    passed: int
    total: int


class User(BaseModel):
    username: str
    attempts: List[Attempt] = []