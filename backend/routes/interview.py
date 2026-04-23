from fastapi import APIRouter
from pydantic import BaseModel

from services.test_runner import run_tests
from services.interviewer import generate_followups, next_difficulty
from services.plagiarism import check_plagiarism
from services.question_bank import get_random_question

router = APIRouter()


# =========================
# 📦 MODEL
# =========================
class AnswerInput(BaseModel):
    code: str
    question: str
    difficulty: str


# =========================
# 🎲 GET RANDOM QUESTION
# =========================
@router.get("/questions/{difficulty}")
def get_questions(difficulty: str):
    return [get_random_question(difficulty)]


# =========================
# 🧪 EVALUATION ENGINE
# =========================
@router.post("/evaluate")
def evaluate_answer(data: AnswerInput):
    code = data.code
    question = data.question.lower()

    # 1️⃣ RUN TESTS
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
    passed = sum(1 for r in results if r.get("status") == "PASS")

    test_score = (passed / total) * 70 if total > 0 else 0

    # 2️⃣ CODE QUALITY (30)
    code_lower = code.lower()
    quality_score = 0

    if "def " in code_lower:
        quality_score += 5
    if "return" in code_lower:
        quality_score += 5
    if "for " in code_lower or "while " in code_lower:
        quality_score += 5
    if "if " in code_lower:
        quality_score += 5
    if len(code.strip()) > 50:
        quality_score += 5
    if "try" in code_lower:
        quality_score += 5

    final_score = int(test_score + quality_score)

    # 3️⃣ VERDICT
    if final_score >= 85:
        verdict = "Hire ✅"
    elif final_score >= 60:
        verdict = "Borderline ⚠️"
    else:
        verdict = "Reject ❌"

    # 4️⃣ FEEDBACK
    feedback = []

    if passed == total:
        feedback.append("All test cases passed ✔️")
    else:
        feedback.append(f"{passed}/{total} test cases passed")

    if "if" not in code_lower:
        feedback.append("Missing edge case handling")

    if "for" not in code_lower and "while" not in code_lower:
        feedback.append("No iteration logic detected")

    if len(code.strip()) < 30:
        feedback.append("Code too short")

    if not feedback:
        feedback.append("Strong solution overall 🚀")

    # 5️⃣ FOLLOWUPS (SERVICE)
    followups = generate_followups(code, question, passed, total)

    # 6️⃣ PLAGIARISM
    plagiarism = check_plagiarism(code)

    # 7️⃣ NEXT DIFFICULTY
    next_diff = next_difficulty(data.difficulty, final_score)

    return {
        "score": final_score,
        "verdict": verdict,
        "feedback": " | ".join(feedback),
        "passed": passed,
        "total": total,
        "followups": followups,
        "plagiarism": plagiarism,
        "next_difficulty": next_diff
    }