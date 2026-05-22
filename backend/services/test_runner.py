import traceback
import time

TEST_CASES = {
    # ── EASY ────────────────────────────────────────────────
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
            {"input": "level", "expected": True},
            {"input": "world", "expected": False},
        ],
    },
    "Factorial": {
        "public": [
            {"input": 5, "expected": 120},
            {"input": 0, "expected": 1},
        ],
        "hidden": [
            {"input": 1, "expected": 1},
            {"input": 3, "expected": 6},
        ],
    },
    "Fibonacci Number": {
        "public": [
            {"input": 0, "expected": 0},
            {"input": 1, "expected": 1},
        ],
        "hidden": [
            {"input": 5, "expected": 5},
            {"input": 10, "expected": 55},
        ],
    },
    "Sum of Digits": {
        "public": [
            {"input": 123, "expected": 6},
            {"input": 456, "expected": 15},
        ],
        "hidden": [
            {"input": 0, "expected": 0},
            {"input": 999, "expected": 27},
        ],
    },
    "Count Vowels": {
        "public": [
            {"input": "hello", "expected": 2},
            {"input": "aeiou", "expected": 5},
        ],
        "hidden": [
            {"input": "", "expected": 0},
            {"input": "rhythm", "expected": 0},
        ],
    },
    "Max in List": {
        "public": [
            {"input": [3, 1, 4, 1, 5, 9], "expected": 9},
            {"input": [1, 2, 3], "expected": 3},
        ],
        "hidden": [
            {"input": [-1, -2, -3], "expected": -1},
            {"input": [42], "expected": 42},
        ],
    },
    "Min in List": {
        "public": [
            {"input": [3, 1, 4, 1, 5], "expected": 1},
            {"input": [10, 20, 5], "expected": 5},
        ],
        "hidden": [
            {"input": [-1, -2, -3], "expected": -3},
            {"input": [7], "expected": 7},
        ],
    },
    "Even or Odd": {
        "public": [
            {"input": 4, "expected": "Even"},
            {"input": 7, "expected": "Odd"},
        ],
        "hidden": [
            {"input": 0, "expected": "Even"},
            {"input": 1, "expected": "Odd"},
        ],
    },
    "Remove Spaces": {
        "public": [
            {"input": "hello world", "expected": "helloworld"},
            {"input": "a b c", "expected": "abc"},
        ],
        "hidden": [
            {"input": "", "expected": ""},
            {"input": "no spaces", "expected": "nospaces"},
        ],
    },
    "Count Words": {
        "public": [
            {"input": "hello world", "expected": 2},
            {"input": "one two three four", "expected": 4},
        ],
        "hidden": [
            {"input": "", "expected": 0},
            {"input": "single", "expected": 1},
        ],
    },
    "Square Number": {
        "public": [
            {"input": 4, "expected": 16},
            {"input": 3, "expected": 9},
        ],
        "hidden": [
            {"input": 0, "expected": 0},
            {"input": 10, "expected": 100},
        ],
    },
    "Cube Number": {
        "public": [
            {"input": 3, "expected": 27},
            {"input": 2, "expected": 8},
        ],
        "hidden": [
            {"input": 0, "expected": 0},
            {"input": 4, "expected": 64},
        ],
    },
    "Check Prime": {
        "public": [
            {"input": 5, "expected": True},
            {"input": 4, "expected": False},
        ],
        "hidden": [
            {"input": 1, "expected": False},
            {"input": 2, "expected": True},
        ],
    },
    "Find Length": {
        "public": [
            {"input": "hello", "expected": 5},
            {"input": "ab", "expected": 2},
        ],
        "hidden": [
            {"input": "", "expected": 0},
            {"input": "python", "expected": 6},
        ],
    },
    "Uppercase String": {
        "public": [
            {"input": "hello", "expected": "HELLO"},
            {"input": "world", "expected": "WORLD"},
        ],
        "hidden": [
            {"input": "", "expected": ""},
            {"input": "abc123", "expected": "ABC123"},
        ],
    },
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
    "Sum of List": {
        "public": [
            {"input": [1, 2, 3], "expected": 6},
            {"input": [10, 20], "expected": 30},
        ],
        "hidden": [
            {"input": [], "expected": 0},
            {"input": [5], "expected": 5},
        ],
    },
    "Average of List": {
        "public": [
            {"input": [1, 2, 3], "expected": 2.0},
            {"input": [10, 20], "expected": 15.0},
        ],
        "hidden": [
            {"input": [5], "expected": 5.0},
            {"input": [0, 0, 0], "expected": 0.0},
        ],
    },
    "Find Index": {
        "public": [
            {"input": ([1, 2, 3], 2), "expected": 1},
            {"input": ([10, 20, 30], 30), "expected": 2},
        ],
        "hidden": [
            {"input": ([5, 6, 7], 5), "expected": 0},
        ],
    },
    # ── MEDIUM ──────────────────────────────────────────────
    "Two Sum": {
        "public": [
            {"input": ([2, 7, 11, 15], 9), "expected": [0, 1]},
        ],
        "hidden": [
            {"input": ([3, 2, 4], 6), "expected": [1, 2]},
        ],
    },
    "Anagram Check": {
        "public": [
            {"input": ("listen", "silent"), "expected": True},
            {"input": ("hello", "world"), "expected": False},
        ],
        "hidden": [
            {"input": ("", ""), "expected": True},
        ],
    },
    "Second Largest": {
        "public": [
            {"input": [1, 2, 3, 4, 5], "expected": 4},
            {"input": [10, 5, 8], "expected": 8},
        ],
        "hidden": [
            {"input": [1, 1, 2], "expected": 1},
        ],
    },
    "Rotate Array": {
        "public": [
            {"input": ([1, 2, 3, 4, 5], 2), "expected": [4, 5, 1, 2, 3]},
        ],
        "hidden": [
            {"input": ([1, 2, 3], 1), "expected": [3, 1, 2]},
        ],
    },
    "Valid Parentheses": {
        "public": [
            {"input": "()", "expected": True},
            {"input": "()[]{}", "expected": True},
            {"input": "(]", "expected": False},
        ],
        "hidden": [
            {"input": "((", "expected": False},
            {"input": "", "expected": True},
        ],
    },
    # ── HARD ────────────────────────────────────────────────
    "Merge Intervals": {
        "public": [
            {"input": [[1, 3], [2, 6], [8, 10]], "expected": [[1, 6], [8, 10]]},
        ],
        "hidden": [
            {"input": [[1, 4], [4, 5]], "expected": [[1, 5]]},
        ],
    },
    "Trapping Rain Water": {
        "public": [
            {"input": [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], "expected": 6},
        ],
        "hidden": [
            {"input": [4, 2, 0, 3, 2, 5], "expected": 9},
        ],
    },
    "Edit Distance": {
        "public": [
            {"input": ("horse", "ros"), "expected": 3},
        ],
        "hidden": [
            {"input": ("intention", "execution"), "expected": 5},
        ],
    },
}

TIME_LIMIT = 2


def run_tests(code: str, question):
    try:
        local_env = {}
        exec(code, {}, local_env)

        if "solution" not in local_env:
            return {"error": "Function 'solution' not found in your code"}

        func = local_env["solution"]
        q_title = question["title"]
        q_tests = TEST_CASES.get(q_title)

        if not q_tests:
            return {
                "error": f"No test cases defined for '{q_title}' yet.",
                "results": [],
                "passed": 0,
                "total": 0,
            }

        results = []
        passed = 0
        total = 0

        for visibility in ["public", "hidden"]:
            for test in q_tests.get(visibility, []):
                total += 1
                inp = test["input"]

                try:
                    start = time.time()
                    output = func(*inp) if isinstance(inp, tuple) else func(inp)
                    elapsed = time.time() - start

                    if elapsed > TIME_LIMIT:
                        results.append({
                            "input": str(inp) if visibility == "public" else "Hidden",
                            "expected": str(test["expected"]) if visibility == "public" else "Hidden",
                            "output": "Time Limit Exceeded",
                            "passed": False,
                            "type": visibility,
                        })
                        continue

                    is_pass = output == test["expected"]
                    if is_pass:
                        passed += 1

                    results.append({
                        "input": str(inp) if visibility == "public" else "Hidden",
                        "expected": str(test["expected"]) if visibility == "public" else "Hidden",
                        "output": str(output) if visibility == "public" else "Hidden",
                        "passed": is_pass,
                        "type": visibility,
                    })

                except Exception as e:
                    results.append({
                        "input": str(inp) if visibility == "public" else "Hidden",
                        "expected": str(test["expected"]) if visibility == "public" else "Hidden",
                        "output": str(e),
                        "passed": False,
                        "type": visibility,
                    })

        return {"results": results, "passed": passed, "total": total}

    except SyntaxError as e:
        return {"error": f"Syntax error: {e}"}
    except Exception:
        return {"error": traceback.format_exc()}