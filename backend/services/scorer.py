def score_code(code: str):
    score = 0
    feedback = []

    if "for" in code or "while" in code:
        score += 2
    else:
        feedback.append("No iteration used — check logic completeness")

    if "if" in code:
        score += 2
    else:
        feedback.append("No condition handling")

    if len(code) > 50:
        score += 2
    else:
        feedback.append("Solution too short — may be incomplete")

    if "print" not in code:
        score += 2
    else:
        feedback.append("Avoid print statements in final submission")

    final_score = score * 10  # out of 80

    verdict = "Hire ✅" if final_score >= 50 else "Reject ❌"

    return {
        "score": final_score,
        "feedback": feedback,
        "verdict": verdict
    }

def calculate_score(results, code):
    total = len(results)
    passed = sum(1 for r in results if r.get("status") == "PASS")

    score = int((passed / total) * 70)

    if "for" in code or "while" in code:
        score += 10

    if len(code) > 50:
        score += 10

    score = min(score, 100)

    if score >= 80:
        verdict = "Hire ✅"
    elif score >= 50:
        verdict = "Borderline ⚠️"
    else:
        verdict = "Reject ❌"

    return {
        "score": score,
        "passed": passed,
        "total": total,
        "verdict": verdict
    }