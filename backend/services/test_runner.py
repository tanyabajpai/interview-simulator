import traceback

def run_tests(code: str, question: str):
    try:
        local_env = {}

        # Execute user code safely
        exec(code, {}, local_env)

        question = question.lower()

        # ✅ Always expect solution()
        func = local_env.get("solution")
        if not callable(func):
            return {
                "results": [],
                "error": "solution() function not found or invalid"
            }

        # =========================
        # TEST CASES
        # =========================
        if "fibonacci" in question:
            test_cases = [
                (0, 0),
                (1, 1),
                (5, 5),
                (10, 55),
            ]

        elif "palindrome" in question:
            test_cases = [
                ("racecar", True),
                ("hello", False),
                ("A man, a plan, a canal: Panama", True),
            ]

        elif "reverse" in question:
            test_cases = [
                ("hello", "olleh"),
                ("abc", "cba"),
                ("", ""),
                ("a", "a"),
                ("123", "321"),
            ]

        elif "factorial" in question:
            test_cases = [
                (0, 1),
                (1, 1),
                (5, 120),
                (7, 5040),
            ]

        else:
            return {
                "results": [],
                "error": f"Unknown question: {question}"
            }

        # =========================
        # RUN TESTS
        # =========================
        results = []

        for inp, expected in test_cases:
            try:
                output = func(inp)

                passed = output == expected

                results.append({
                    "input": inp,
                    "expected": expected,
                    "output": output,
                    "passed": passed
                })

            except Exception as e:
                results.append({
                    "input": inp,
                    "expected": expected,
                    "output": None,
                    "error": str(e),
                    "passed": False
                })

        return {"results": results}

    except Exception:
        return {
            "results": [],
            "error": traceback.format_exc()
        }