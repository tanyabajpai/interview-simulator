
def calculate_score(results, code):
    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))

    score = int((passed / total) * 100) if total > 0 else 0

    if score == 100:
        verdict = "Accepted ✅"
    elif score >= 50:
        verdict = "Partial ⚠️"
    else:
        verdict = "Reject ❌"

    return {
        "score": score,
        "passed": passed,
        "total": total,
        "verdict": verdict
    }