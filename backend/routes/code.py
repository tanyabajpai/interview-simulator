from fastapi import APIRouter
from pydantic import BaseModel
from services.code_execution import run_code
from services.test_runner import run_tests
from services.scorer import calculate_score  # ✅ USE THIS

router = APIRouter()


class CodeRequest(BaseModel):
    code: str
    question: str | None = None


# ▶ RUN CODE
@router.post("/run")
def execute_code(data: CodeRequest):
    result = run_code(data.code)

    return {
        "output": result.get("stdout", ""),
        "error": result.get("stderr", "")
    }


# 🧪 RUN TESTS (FINAL CLEAN)
@router.post("/test")
def test_code(data: CodeRequest):
    result = run_tests(data.code, data.question)

    # ❌ If execution error
    if "error" in result:
        return {
            "results": [],
            "score": 0,
            "verdict": "Error ❌",
            "error": result["error"]
        }

    results = result.get("results", [])

    # ✅ SINGLE SOURCE OF TRUTH
    from services.scorer import calculate_score

@router.post("/test")
def test_code(data: CodeRequest):
    result = run_tests(data.code, data.question)

    if "error" in result:
        return {
            "results": [],
            "score": 0,
            "verdict": "Error ❌",
            "error": result["error"]
        }

    results = result.get("results", [])

    # ✅ FIX: use calculated score properly
    score_data = calculate_score(results, data.code)

    return {
        "results": results,
        "score": score_data["score"],
        "verdict": score_data["verdict"]
    }
   