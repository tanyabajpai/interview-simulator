import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_ai_feedback(code: str, question: str):
    feedback = []

    code_lower = code.lower()

    # =========================
    # 🧠 LOGIC ANALYSIS
    # =========================
    if "for" in code_lower or "while" in code_lower:
        feedback.append("Uses iteration effectively ✔️")
    else:
        feedback.append("No loops detected — verify logic")

    if "if" in code_lower:
        feedback.append("Handles conditions ✔️")
    else:
        feedback.append("Missing conditional checks (edge cases?)")

    if "return" not in code_lower:
        feedback.append("Missing return statement ❌")

    # =========================
    # ⚡ PERFORMANCE
    # =========================
    if "sort" in code_lower:
        feedback.append("Sorting used — may increase time complexity (O(n log n))")

    if code_lower.count("for") > 1:
        feedback.append("Nested loops detected — could be O(n²)")

    # =========================
    # 🧩 EDGE CASES
    # =========================
    if "len" not in code_lower and "==" not in code_lower:
        feedback.append("Edge cases not clearly handled")

    if "try" in code_lower:
        feedback.append("Good use of exception handling ✔️")

    # =========================
    # 🧹 CLEAN CODE
    # =========================
    if len(code.strip()) < 40:
        feedback.append("Code too short — may lack robustness")

    if " " * 4 not in code:
        feedback.append("Indentation could be improved")

    # =========================
    # 🎯 QUESTION-SPECIFIC FEEDBACK
    # =========================
    if "palindrome" in question:
        if "[::-1]" in code:
            feedback.append("Efficient use of slicing ✔️")
        if "isalnum" not in code_lower:
            feedback.append("Consider ignoring special characters")

    if "reverse" in question:
        if "[::-1]" in code:
            feedback.append("Pythonic solution using slicing ✔️")

    if "factorial" in question:
        if "recursion" in code_lower:
            feedback.append("Recursive approach used ✔️")
        if "for" in code_lower:
            feedback.append("Iterative approach is efficient ✔️")

    if not feedback:
        feedback.append("Clean and efficient solution 🚀")

    return " | ".join(feedback)