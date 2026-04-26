import traceback
import time


# =========================
# 🧪 TEST CASE STRUCTURE (LEETCODE STYLE)
# =========================
TEST_CASES = {
    "Reverse String": {
        "public": [
            {"input": "hello", "expected": "olleh"},
            {"input": "abc", "expected": "cba"},
        ],
        "hidden": [
            {"input": "", "expected": ""},
            {"input": "a", "expected": "a"},
        ],
    },

    "Palindrome Check": {
        "public": [
            {"input": "racecar", "expected": True},
            {"input": "hello", "expected": False},
        ],
        "hidden": [
            {"input": "A man a plan a canal Panama", "expected": True},
        ],
    },

    "Factorial": {
        "public": [
            {"input": 5, "expected": 120},
            {"input": 0, "expected": 1},
        ],
        "hidden": [
            {"input": 1, "expected": 1},
        ],
    },

    "Two Sum": {
        "public": [
            {"input": ([2, 7, 11, 15], 9), "expected": [0, 1]},
        ],
        "hidden": [
            {"input": ([3, 2, 4], 6), "expected": [1, 2]},
        ],
    },

    # ✅ ADD THIS
    "Lowercase String": {
        "public": [
            {"input": "HELLO", "expected": "hello"},
            {"input": "Python", "expected": "python"},
        ],
        "hidden": [
            {"input": "", "expected": ""},
            {"input": "ABC123", "expected": "abc123"},
        ],
    },

    # ✅ ADD MORE (IMPORTANT)
    "Find Length": {
        "public": [
            {"input": "hello", "expected": 5},
        ],
        "hidden": [
            {"input": "", "expected": 0},
        ],
    },

    "Square Number": {
        "public": [
            {"input": 4, "expected": 16},
        ],
        "hidden": [
            {"input": 0, "expected": 0},
        ],
    },

    "Check Prime": {
        "public": [
            {"input": 5, "expected": True},
            {"input": 4, "expected": False},
        ],
        "hidden": [
            {"input": 1, "expected": False},
        ],
    },
}


# =========================
# ⚡ TIME LIMIT (seconds)
# =========================
TIME_LIMIT = 2


# =========================
# 🚀 EXECUTION ENGINE
# =========================
def run_tests(code: str, question):
    try:
        local_env = {}

        # 🔥 execute user code
        exec(code, {}, local_env)

        # =========================
        # ❌ function missing
        # =========================
        if "solution" not in local_env:
            return {"error": "Function 'solution' not found"}

        func = local_env["solution"]

        q_title = question["title"]
        q_tests = TEST_CASES.get(q_title)

        if not q_tests:
            return {"error": "No test cases found for this question"}

        results = []
        passed = 0
        total = 0

        # =========================
        # 🧪 RUN TESTS
        # =========================
        for visibility in ["public", "hidden"]:
            for test in q_tests[visibility]:
                total += 1

                try:
                    start = time.time()

                    inp = test["input"]

                    if isinstance(inp, tuple):
                        output = func(*inp)
                    else:
                        output = func(inp)

                    exec_time = time.time() - start

                    # ⏱️ TIME LIMIT CHECK
                    if exec_time > TIME_LIMIT:
                        results.append({
                            "input": inp,
                            "expected": test["expected"],
                            "output": "Time Limit Exceeded",
                            "passed": False,
                            "type": visibility
                        })
                        continue

                    is_pass = output == test["expected"]

                    if is_pass:
                        passed += 1

                    results.append({
                        "input": inp if visibility == "public" else "Hidden",
                        "expected": test["expected"] if visibility == "public" else "Hidden",
                        "output": output if visibility == "public" else "Hidden",
                        "passed": is_pass,
                        "type": visibility
                    })

                except Exception as e:
                    results.append({
                        "input": test["input"],
                        "expected": test["expected"],
                        "output": str(e),
                        "passed": False,
                        "type": visibility
                    })

        return {
            "results": results,
            "passed": passed,
            "total": total
        }

    except Exception:
        return {"error": traceback.format_exc()}