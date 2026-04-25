users_db = {}


def save_attempt(username, attempt):
    if username not in users_db:
        users_db[username] = []

    users_db[username].append(attempt)


def get_user_attempts(username):
    return users_db.get(username, [])


def get_user_stats(username):
    attempts = users_db.get(username, [])

    total_attempts = len(attempts)

    if total_attempts == 0:
        return {
            "total_attempts": 0,
            "avg_score": 0,
            "accuracy": 0
        }

    total_score = sum(a["score"] for a in attempts)
    total_passed = sum(a["passed"] for a in attempts)
    total_tests = sum(a["total"] for a in attempts)

    return {
        "total_attempts": total_attempts,
        "avg_score": total_score // total_attempts,
        "accuracy": int((total_passed / total_tests) * 100) if total_tests else 0
    }