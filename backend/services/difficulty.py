def next_difficulty(current: str, score: int):
    if score >= 85:
        if current == "easy":
            return "medium"
        if current == "medium":
            return "hard"

    if score < 50:
        return "easy"

    return current