from fastapi import APIRouter
from pydantic import BaseModel
from services.code_execution import run_code
from services.test_runner import run_tests

router = APIRouter()

class CodeRequest(BaseModel):
    code: str
    question: str = "fibonacci"

# ▶ RUN CODE
@router.post("/run")
def execute_code(data: CodeRequest):
    result = run_code(data.code)

    return {
        "stdout": result.get("stdout", ""),
        "stderr": result.get("stderr", "")
    }

# 🧪 RUN TESTS (FIXED)
@router.post("/test")
def test_code(data: CodeRequest):
    result = run_tests(data.code, data.question)

    if isinstance(result, dict) and "error" in result:
        return {"results": [result]}

    return {
        "results": result.get("results", []),
        "score": result.get("score", {})
    }