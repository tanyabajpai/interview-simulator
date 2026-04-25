import traceback


# =========================
# 🧪 TEST CASE BANK (REAL)
# =========================
TEST_CASES = {
    "Reverse String": [
        {"input": "hello", "expected": "olleh"},
        {"input": "abc", "expected": "cba"},
        {"input": "", "expected": ""},
        {"input": "a", "expected": "a"},
    ],

    "Palindrome Check": [
        {"input": "racecar", "expected": True},
        {"input": "hello", "expected": False},
        {"input": "A man a plan a canal Panama", "expected": True},
    ],

    "Factorial": [
        {"input": 5, "expected": 120},
        {"input": 0, "expected": 1},
        {"input": 1, "expected": 1},
    ],

    "Fibonacci Number": [
        {"input": 5, "expected": 5},
        {"input": 0, "expected": 0},
        {"input": 1, "expected": 1},
    ],

    "Sum of Digits": [
        {"input": 123, "expected": 6},
        {"input": 0, "expected": 0},
    ],

    "Count Vowels": [
        {"input": "hello", "expected": 2},
        {"input": "xyz", "expected": 0},
    ],

    "Max in List": [
        {"input": [1, 5, 2], "expected": 5},
        {"input": [-1, -5, -2], "expected": -1},
    ],

    "Min in List": [
        {"input": [1, 5, 2], "expected": 1},
        {"input": [-1, -5, -2], "expected": -5},
    ],

    "Even or Odd": [
        {"input": 2, "expected": "Even"},
        {"input": 3, "expected": "Odd"},
    ],

    "Remove Spaces": [
        {"input": "hello world", "expected": "helloworld"},
        {"input": " a b ", "expected": "ab"},
    ],

    "Count Words": [
        {"input": "hello world", "expected": 2},
        {"input": "", "expected": 0},
    ],

    "Square Number": [
        {"input": 4, "expected": 16},
        {"input": -2, "expected": 4},
    ],

    "Cube Number": [
        {"input": 3, "expected": 27},
        {"input": -2, "expected": -8},
    ],

    "Check Prime": [
        {"input": 2, "expected": True},
        {"input": 4, "expected": False},
        {"input": 17, "expected": True},
    ],

    "Find Length": [
        {"input": "hello", "expected": 5},
        {"input": "", "expected": 0},
    ],

    "Uppercase String": [
        {"input": "hello", "expected": "HELLO"},
    ],

    "Lowercase String": [
        {"input": "HELLO", "expected": "hello"},
    ],

    "Sum of List": [
        {"input": [1, 2, 3], "expected": 6},
    ],

    "Average of List": [
        {"input": [2, 4, 6], "expected": 4},
    ],

    "Find Index": [
        {"input": ([1, 2, 3], 2), "expected": 1},
    ],

    # =========================
    # MEDIUM
    # =========================

    "Two Sum": [
        {"input": ([2, 7, 11, 15], 9), "expected": [0, 1]},
    ],

    "Anagram Check": [
        {"input": ("listen", "silent"), "expected": True},
        {"input": ("hello", "world"), "expected": False},
    ],

    "Second Largest": [
        {"input": [1, 5, 3], "expected": 3},
    ],

    "Rotate Array": [
        {"input": ([1, 2, 3, 4], 1), "expected": [4, 1, 2, 3]},
    ],

    "Valid Parentheses": [
        {"input": "()", "expected": True},
        {"input": "(]", "expected": False},
    ],

    # =========================
    # HARD
    # =========================

    "Merge Intervals": [
        {"input": [[1, 3], [2, 6]], "expected": [[1, 6]]},
    ],

    "Trapping Rain Water": [
        {"input": [0,1,0,2,1,0,1,3], "expected": 6},
    ],
}


# =========================
# 🚀 EXECUTION ENGINE
# =========================
def run_tests(code: str, question):
    try:
        # 🔥 run user code
        local_env = {}
        exec(code, {}, local_env)

        if "solution" not in local_env:
            return {"error": "Function 'solution' not found"}

        func = local_env["solution"]

        test_cases = TEST_CASES.get(question["title"], [])

        results = []

        for test in test_cases:
            try:
                inp = test["input"]

                if isinstance(inp, tuple):
                    output = func(*inp)
                else:
                    output = func(inp)

                passed = output == test["expected"]

                results.append({
                    "input": inp,
                    "expected": test["expected"],
                    "output": output,
                    "passed": passed
                })

            except Exception as e:
                results.append({
                    "input": test["input"],
                    "expected": test["expected"],
                    "output": str(e),
                    "passed": False
                })

        return {"results": results}

    except Exception:
        return {"error": traceback.format_exc()}