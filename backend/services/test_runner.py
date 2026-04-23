import traceback

def run_tests(code: str, question: str):
    results = []

    try:
        local_env = {}

        # Execute user code
        exec(code, {}, local_env)

        question = question.lower()

        # =========================
        # 🧠 AUTO DETECT FUNCTION
        # =========================

        if "fibonacci" in question:
            func_name = "fibonacci"
            test_cases = [
                {"input": 0, "expected": 0},
                {"input": 1, "expected": 1},
                {"input": 5, "expected": 5},
                {"input": 10, "expected": 55},
            ]

        elif "palindrome" in question:
            func_name = "is_palindrome"
            test_cases = [
                {"input": "racecar", "expected": True},
                {"input": "hello", "expected": False},
                {"input": "A man, a plan, a canal: Panama", "expected": True},
            ]

        elif "reverse" in question:
            func_name = "reverse_string"
            test_cases = [
                {"input": "hello", "expected": "olleh"},
                {"input": "abc", "expected": "cba"},
                {"input": "", "expected": ""},
                {"input": "a", "expected": "a"},
                {"input": "123", "expected": "321"},
            ]

        elif "factorial" in question:
            func_name = "factorial"
            test_cases = [
                {"input": 0, "expected": 1},
                {"input": 1, "expected": 1},
                {"input": 5, "expected": 120},
                {"input": 7, "expected": 5040},
            ]

        else:
            return {
                "results": [],
                "error": f"Unknown question: {question}"
            }

        func = local_env.get(func_name)

        if not func:
            return {
                "results": [],
                "error": f"{func_name} function not found"
            }

        # =========================
        # 🧪 RUN TESTS
        # =========================
        for t in test_cases:
            try:
                output = func(t["input"])
                status = "PASS" if output == t["expected"] else "FAIL"

                results.append({
                    "input": t["input"],
                    "expected": t["expected"],
                    "output": output,
                    "status": status
                })

            except Exception as e:
                results.append({
                    "input": t["input"],
                    "error": str(e),
                    "status": "FAIL"
                })

        return {"results": results}

    except Exception:
        return {"error": traceback.format_exc()}