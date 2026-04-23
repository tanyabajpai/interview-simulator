from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class FeedbackRequest(BaseModel):
    code: str
    question: str


# =========================
# 🤖 ELITE AI CODE REVIEW ENGINE
# =========================
@router.post("/feedback")
def get_feedback(data: FeedbackRequest):
    code = data.code
    code_lower = code.lower()
    question = data.question.lower()

    feedback = []

    # =========================
    # 🧠 LOGIC CHECK
    # =========================
    if "for" in code_lower or "while" in code_lower:
        feedback.append("✅ Uses iteration effectively")
    else:
        feedback.append("⚠️ No iteration detected — verify logic")

    if "if" in code_lower:
        feedback.append("✅ Handles conditions")
    else:
        feedback.append("❌ Missing conditional checks (edge cases not handled)")

    if "return" in code_lower:
        feedback.append("✅ Returns output properly")
    else:
        feedback.append("❌ Missing return statement")

    if "def " in code_lower:
        feedback.append("✅ Proper function structure")

    # =========================
    # ⚡ SMART COMPLEXITY ANALYSIS
    # =========================
    loop_count = code_lower.count("for") + code_lower.count("while")

    if loop_count >= 2:
        # 🔥 Detect two-pointer (NOT O(n²))
        if "left" in code_lower and "right" in code_lower:
            feedback.append("✅ Two-pointer pattern detected → O(n) optimal")
        else:
            feedback.append("⚠️ Multiple loops detected → possible O(n²)")

    if "sort" in code_lower:
        feedback.append("⚠️ Sorting used → O(n log n), check if optimal")

    # =========================
    # 🧩 EDGE CASE INTELLIGENCE (SMART)
    # =========================
    if "none" not in code_lower:
        feedback.append("⚠️ No handling for None input")

    if '""' not in code and "len(" not in code_lower:
        feedback.append("⚠️ Empty input case not clearly handled")

    if "try" not in code_lower:
        feedback.append("⚠️ No error handling (try/except missing)")

    # smarter detection
    if "strip" not in code_lower and "isalnum" not in code_lower:
        feedback.append("⚠️ Input sanitization missing")

    # =========================
    # 🎯 QUESTION-SPECIFIC INTELLIGENCE
    # =========================
    if "palindrome" in question:
        if "isalnum" in code_lower:
            feedback.append("✅ Handles special characters correctly")

        if "[::-1]" in code:
            feedback.append("✅ Pythonic slicing approach")

        if "left" in code_lower and "right" in code_lower:
            feedback.append("✅ Two-pointer approach (best practice)")

    if "reverse" in question:
        if "[::-1]" in code:
            feedback.append("✅ Clean Pythonic solution")

        if "list(" in code_lower and "join" in code_lower:
            feedback.append("✅ Manual reversal shows good control")

    if "factorial" in question:
        if "for" in code_lower:
            feedback.append("✅ Iterative factorial is efficient")

        if "return 1" in code_lower:
            feedback.append("✅ Base case handled correctly")

        if "recursion" in code_lower or "factorial(" in code_lower:
            feedback.append("⚠️ Recursive approach → stack overhead risk")

    # =========================
    # 🧹 CODE QUALITY
    # =========================
    if len(code.strip()) < 40:
        feedback.append("⚠️ Code too short — may miss edge cases")

    if code.count("\n") > 15:
        feedback.append("⚠️ Code slightly long — consider simplifying")

    # =========================
    # 🚀 FINAL VERDICT
    # =========================
    negatives = [f for f in feedback if "❌" in f]

    if len(negatives) == 0:
        feedback.append("🚀 Strong solution — interview ready")
    elif len(negatives) <= 2:
        feedback.append("👍 Decent solution but can be improved")
    else:
        feedback.append("⚠️ Needs improvement — revise fundamentals")

    return {
        "feedback": " | ".join(feedback)
    }


# =========================
# 🎲 RANDOM QUESTION GENERATOR
# =========================
@router.post("/generate-question")
def generate_question():
    return {
        "question": {
            "title": "Find Missing Number",
            "key": "missing_number",
            "difficulty": "medium",
            "description": "Find missing number in array",
            "time": 900,
        }
    }