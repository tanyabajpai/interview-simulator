from fastapi import APIRouter
from pydantic import BaseModel
from services.code_execution import run_code
from services.test_runner import run_tests
from services.scorer import calculate_score  # ✅ USE THIS
from services.question_bank import QUESTION_BANK

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

    # 🔥 find full question object
    all_questions = (
        QUESTION_BANK["easy"] +
        QUESTION_BANK["medium"] +
        QUESTION_BANK["hard"]
    )

    question_obj = next(
        (q for q in all_questions if q["title"] == data.question),
        None
    )

    if not question_obj:
        return {"error": "Question not found"}

    result = run_tests(data.code, question_obj)

    if "error" in result:
        return {"results": [], "score": 0, "error": result["error"]}

    results = result["results"]

    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))

    score = int((passed / total) * 100) if total > 0 else 0

    return {
        "results": results,
        "score": score
    }