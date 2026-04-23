import difflib

# fake DB (later replace with real DB)
submitted_codes = []

def check_plagiarism(new_code: str):
    max_similarity = 0

    for old_code in submitted_codes:
        similarity = difflib.SequenceMatcher(None, new_code, old_code).ratio()
        max_similarity = max(max_similarity, similarity)

    submitted_codes.append(new_code)

    return {
        "similarity": round(max_similarity * 100, 2),
        "flag": max_similarity > 0.8
    }