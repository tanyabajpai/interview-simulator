from fastapi import APIRouter
from pydantic import BaseModel

from services.test_runner import run_tests
from services.interviewer import generate_followups, next_difficulty
from services.plagiarism import check_plagiarism

router = APIRouter()


# =========================
# 📦 MODEL
# =========================
class AnswerInput(BaseModel):
    code: str
    question: str
    difficulty: str


# =========================
# 🧪 EVALUATION ENGINE
# =========================
@router.post("/evaluate")
def evaluate_answer(data: AnswerInput):
    code = data.code
    question = data.question.lower()

    # =========================
    # 1️⃣ RUN TESTS
    # =========================
    test_result = run_tests(code, question)

    if "error" in test_result:
        return {
            "score": 0,
            "verdict": "Error ❌",
            "feedback": test_result["error"],
            "followups": [],
            "plagiarism": {"similarity": 0, "flag": False},
            "next_difficulty": data.difficulty
        }

    results = test_result.get("results", [])
    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))

    # =========================
    # ✅ CLEAN SCORING (NO HARDCODED QUESTIONS)
    # =========================
    score = int((passed / total) * 100) if total > 0 else 0

    if score == 100:
        verdict = "Accepted ✅"
    elif score >= 50:
        verdict = "Partial ⚠️"
    else:
        verdict = "Reject ❌"

    # =========================
    # FEEDBACK
    # =========================
    feedback = (
        f"{passed}/{total} test cases passed"
        if passed != total
        else "All test cases passed ✔️"
    )

    # =========================
    # FOLLOWUPS + OTHER SERVICES
    # =========================
    followups = generate_followups(code, question, passed, total)
    plagiarism = check_plagiarism(code)
    next_diff = next_difficulty(data.difficulty, score)

    return {
        "score": score,
        "verdict": verdict,
        "feedback": feedback,
        "passed": passed,
        "total": total,
        "followups": followups,
        "plagiarism": plagiarism,
        "next_difficulty": next_diff
    }