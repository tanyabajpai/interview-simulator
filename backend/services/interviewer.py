def generate_followups(code: str, question: str, passed: int, total: int):
    code_lower = code.lower()
    followups = []

    # =========================
    # 🧠 BASED ON PERFORMANCE
    # =========================
    if passed == total:
        followups.append("Can you optimize this solution further?")
        followups.append("What is the time and space complexity?")
    else:
        followups.append("Why did some test cases fail?")
        followups.append("How would you debug your solution?")

    # =========================
    # 🔍 CODE ANALYSIS
    # =========================
    if "for" in code_lower or "while" in code_lower:
        followups.append("Can this be solved without iteration?")

    if "recursion" in code_lower:
        followups.append("What is recursion stack complexity?")

    if "if" not in code_lower:
        followups.append("How are edge cases handled?")

    if len(code.strip()) < 40:
        followups.append("Explain your approach in more detail")

    # =========================
    # 🎯 QUESTION-SPECIFIC
    # =========================
    if "palindrome" in question:
        followups.append("How would you ignore special characters?")
        followups.append("Can you do this in O(1) space?")

    if "reverse" in question:
        followups.append("Can you reverse without extra space?")
        followups.append("What is time complexity?")

    if "factorial" in question:
        followups.append("Can you implement using recursion?")
        followups.append("What happens for very large inputs?")

    if not followups:
        followups.append("Explain your approach and complexity")

    return followups


# =========================
# 📈 DIFFICULTY PROGRESSION
# =========================
def next_difficulty(current: str, score: int):
    if score >= 85:
        if current == "easy":
            return "medium"
        elif current == "medium":
            return "hard"

    if score < 50:
        return "easy"

    return current
