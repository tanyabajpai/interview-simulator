from fastapi import APIRouter
from pydantic import BaseModel

from services.test_runner import run_tests
from services.interviewer import generate_followups, next_difficulty
from services.plagiarism import check_plagiarism
from services.question_bank import QUESTION_BANK
from services.user_service import save_attempt
from services.db import attempts_collection

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
    question_title = data.question

    # =========================
    # 🔍 FIND QUESTION OBJECT
    # =========================
    all_questions = (
        QUESTION_BANK["easy"] +
        QUESTION_BANK["medium"] +
        QUESTION_BANK["hard"]
    )

    question_obj = next(
        (q for q in all_questions if q["title"] == question_title),
        None
    )

    if not question_obj:
        return {
            "score": 0,
            "verdict": "Error ❌",
            "feedback": "Question not found",
            "followups": [],
            "plagiarism": {"similarity": 0, "flag": False},
            "next_difficulty": data.difficulty
        }

    # =========================
    # 1️⃣ RUN TESTS
    # =========================
    test_result = run_tests(code, question_obj)

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
    # 2️⃣ SCORING
    # =========================
    test_score = (passed / total) * 80 if total > 0 else 0

    quality_score = 0
    code_lower = code.lower()

    if "for" in code_lower or "while" in code_lower:
        quality_score += 5
    if "if" in code_lower:
        quality_score += 5
    if "return" in code_lower:
        quality_score += 5
    if "def" in code_lower:
        quality_score += 5

    final_score = int(test_score + quality_score)

    # =========================
    # 3️⃣ VERDICT (FIXED)
    # =========================
    if final_score >= 85:
        verdict = "Hire ✅"
    elif final_score >= 60:
        verdict = "Borderline ⚠️"
    else:
        verdict = "Reject ❌"

    # =========================
    # 4️⃣ FEEDBACK
    # =========================
    if passed == total:
        feedback = "All test cases passed ✔️"
    else:
        feedback = f"{passed}/{total} test cases passed"

    # =========================
    # 5️⃣ SERVICES
    # =========================
    followups = generate_followups(code, question_title, passed, total)
    plagiarism = check_plagiarism(code)
    next_diff = next_difficulty(data.difficulty, final_score)

    # =========================
    # 💾 SAVE USER PROGRESS
    # =========================
    save_attempt(
        "guest",  # later replace with real auth
        {
            "question": question_title,
            "score": final_score,
            "passed": passed,
            "total": total
        }
    )

    attempts_collection.insert_one({
    "username": "guest",  # later from token
    "question": question_title,
    "score": final_score,
    "passed": passed,
    "total": total
        }
    )

    # =========================
    # ✅ FINAL RESPONSE (FIXED)
    # =========================
    return {
        "score": final_score,   # ✅ FIXED
        "verdict": verdict,     # ✅ FIXED
        "feedback": feedback,
        "passed": passed,
        "total": total,
        "followups": followups,
        "plagiarism": plagiarism,
        "next_difficulty": next_diff
    }