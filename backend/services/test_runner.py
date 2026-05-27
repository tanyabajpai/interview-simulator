import traceback
import time

TIME_LIMIT = 2

TEST_CASES = {
    # ── EASY ──────────────────────────────────────────────
    "Reverse String": {
        "public":  [{"input": "hello", "expected": "olleh"}, {"input": "abc", "expected": "cba"}],
        "hidden":  [{"input": "", "expected": ""}, {"input": "a", "expected": "a"}],
    },
    "Palindrome Check": {
        "public":  [{"input": "racecar", "expected": True}, {"input": "hello", "expected": False}],
        "hidden":  [{"input": "level", "expected": True}, {"input": "world", "expected": False}],
    },
    "Factorial": {
        "public":  [{"input": 5, "expected": 120}, {"input": 0, "expected": 1}],
        "hidden":  [{"input": 1, "expected": 1}, {"input": 7, "expected": 5040}],
    },
    "Fibonacci Number": {
        "public":  [{"input": 0, "expected": 0}, {"input": 1, "expected": 1}],
        "hidden":  [{"input": 6, "expected": 8}, {"input": 10, "expected": 55}],
    },
    "Count Vowels": {
        "public":  [{"input": "hello", "expected": 2}, {"input": "aeiou", "expected": 5}],
        "hidden":  [{"input": "", "expected": 0}, {"input": "rhythm", "expected": 0}],
    },
    "Sum of List": {
        "public":  [{"input": [1, 2, 3], "expected": 6}, {"input": [10, 20], "expected": 30}],
        "hidden":  [{"input": [], "expected": 0}, {"input": [5], "expected": 5}],
    },
    "Check Prime": {
        "public":  [{"input": 7, "expected": True}, {"input": 10, "expected": False}],
        "hidden":  [{"input": 2, "expected": True}, {"input": 1, "expected": False}],
    },
    "Max in List": {
        "public":  [{"input": [3, 1, 4, 1, 5, 9], "expected": 9}, {"input": [1, 2, 3], "expected": 3}],
        "hidden":  [{"input": [-1, -2, -3], "expected": -1}, {"input": [42], "expected": 42}],
    },
    "Min in List": {
        "public":  [{"input": [3, 1, 4, 1, 5], "expected": 1}, {"input": [10, 20, 5], "expected": 5}],
        "hidden":  [{"input": [-1, -2, -3], "expected": -3}, {"input": [7], "expected": 7}],
    },
    "Even or Odd": {
        "public":  [{"input": 4, "expected": "Even"}, {"input": 7, "expected": "Odd"}],
        "hidden":  [{"input": 0, "expected": "Even"}, {"input": 1, "expected": "Odd"}],
    },
    "Remove Spaces": {
        "public":  [{"input": "hello world", "expected": "helloworld"}, {"input": "a b c", "expected": "abc"}],
        "hidden":  [{"input": "", "expected": ""}, {"input": "no spaces", "expected": "nospaces"}],
    },
    "Remove Duplicates": {
        "public":  [{"input": [1, 2, 2, 3], "expected": [1, 2, 3]}, {"input": [5, 5, 5], "expected": [5]}],
        "hidden":  [{"input": [], "expected": []}, {"input": [1, 2, 3], "expected": [1, 2, 3]}],
    },
    "Count Words": {
        "public":  [{"input": "hello world", "expected": 2}, {"input": "one two three", "expected": 3}],
        "hidden":  [{"input": "", "expected": 0}, {"input": "single", "expected": 1}],
    },
    "Square Number": {
        "public":  [{"input": 4, "expected": 16}, {"input": 3, "expected": 9}],
        "hidden":  [{"input": 0, "expected": 0}, {"input": 10, "expected": 100}],
    },
    "Cube Number": {
        "public":  [{"input": 3, "expected": 27}, {"input": 2, "expected": 8}],
        "hidden":  [{"input": 0, "expected": 0}, {"input": 4, "expected": 64}],
    },
    "Find Length": {
        "public":  [{"input": "hello", "expected": 5}, {"input": "ab", "expected": 2}],
        "hidden":  [{"input": "", "expected": 0}, {"input": "python", "expected": 6}],
    },
    "Uppercase String": {
        "public":  [{"input": "hello", "expected": "HELLO"}, {"input": "world", "expected": "WORLD"}],
        "hidden":  [{"input": "", "expected": ""}, {"input": "abc123", "expected": "ABC123"}],
    },
    "Lowercase String": {
        "public":  [{"input": "HELLO", "expected": "hello"}, {"input": "Python", "expected": "python"}],
        "hidden":  [{"input": "", "expected": ""}, {"input": "ABC123", "expected": "abc123"}],
    },
    "Average of List": {
        "public":  [{"input": [1, 2, 3, 4, 5], "expected": 3.0}, {"input": [1, 2], "expected": 1.5}],
        "hidden":  [{"input": [10], "expected": 10.0}, {"input": [0, 0, 0], "expected": 0.0}],
    },
    "Find Index": {
        "public":  [{"input": ([1, 2, 3], 2), "expected": 1}, {"input": ([10, 20, 30], 30), "expected": 2}],
        "hidden":  [{"input": ([5, 6, 7], 5), "expected": 0}],
    },
    "FizzBuzz": {
        "public":  [{"input": 5, "expected": ["1","2","Fizz","4","Buzz"]}],
        "hidden":  [{"input": 1, "expected": ["1"]}, {"input": 3, "expected": ["1","2","Fizz"]}],
    },
    "Sum of Digits": {
        "public":  [{"input": 1234, "expected": 10}, {"input": 9, "expected": 9}],
        "hidden":  [{"input": 0, "expected": 0}, {"input": 999, "expected": 27}],
    },
    "Flatten List": {
        "public":  [{"input": [[1, 2], [3, 4], [5]], "expected": [1, 2, 3, 4, 5]}],
        "hidden":  [{"input": [[], [1], [2, 3]], "expected": [1, 2, 3]}, {"input": [[]], "expected": []}],
    },
    "Count Occurrences": {
        "public":  [{"input": ([1, 2, 2, 3, 2], 2), "expected": 3}],
        "hidden":  [{"input": ([1, 2, 3], 5), "expected": 0}, {"input": ([], 1), "expected": 0}],
    },
    "Power Function": {
        "public":  [{"input": (2, 10), "expected": 1024}, {"input": (3, 3), "expected": 27}],
        "hidden":  [{"input": (5, 0), "expected": 1}, {"input": (1, 100), "expected": 1}],
    },
    "Merge Two Sorted Lists": {
        "public":  [{"input": ([1, 3, 5], [2, 4, 6]), "expected": [1, 2, 3, 4, 5, 6]}],
        "hidden":  [{"input": ([], [1, 2]), "expected": [1, 2]}, {"input": ([1], []), "expected": [1]}],
    },
    "Missing Number": {
        "public":  [{"input": [3, 0, 1], "expected": 2}, {"input": [0, 1], "expected": 2}],
        "hidden":  [{"input": [0], "expected": 1}, {"input": [1], "expected": 0}],
    },
    "Is Anagram": {
        "public":  [{"input": ("listen", "silent"), "expected": True}, {"input": ("hello", "world"), "expected": False}],
        "hidden":  [{"input": ("abc", "cab"), "expected": True}, {"input": ("a", "b"), "expected": False}],
    },

    # ── MEDIUM ────────────────────────────────────────────
    "Two Sum": {
        "public":  [{"input": ([2, 7, 11, 15], 9), "expected": [0, 1]}],
        "hidden":  [{"input": ([3, 2, 4], 6), "expected": [1, 2]}, {"input": ([3, 3], 6), "expected": [0, 1]}],
    },
    "Valid Parentheses": {
        "public":  [{"input": "()", "expected": True}, {"input": "()[]{}", "expected": True}, {"input": "(]", "expected": False}],
        "hidden":  [{"input": "((", "expected": False}, {"input": "{[]}", "expected": True}],
    },
    "Longest Substring Without Repeating": {
        "public":  [{"input": "abcabcbb", "expected": 3}, {"input": "bbbbb", "expected": 1}],
        "hidden":  [{"input": "pwwkew", "expected": 3}, {"input": "", "expected": 0}],
    },
    "Second Largest": {
        "public":  [{"input": [3, 1, 4, 1, 5, 9, 2, 6], "expected": 6}],
        "hidden":  [{"input": [1, 1], "expected": -1}, {"input": [5, 3], "expected": 3}],
    },
    "Rotate Array": {
        "public":  [{"input": ([1, 2, 3, 4, 5, 6, 7], 3), "expected": [5, 6, 7, 1, 2, 3, 4]}],
        "hidden":  [{"input": ([-1, -100, 3, 99], 2), "expected": [3, 99, -1, -100]}],
    },
    "Product Except Self": {
        "public":  [{"input": [1, 2, 3, 4], "expected": [24, 12, 8, 6]}],
        "hidden":  [{"input": [2, 3], "expected": [3, 2]}],
    },
    "Top K Frequent Elements": {
        "public":  [{"input": ([1, 1, 1, 2, 2, 3], 2), "expected": [1, 2]}],
        "hidden":  [{"input": ([1], 1), "expected": [1]}],
    },
    "Kth Largest Element": {
        "public":  [{"input": ([3, 2, 1, 5, 6, 4], 2), "expected": 5}],
        "hidden":  [{"input": ([1], 1), "expected": 1}],
    },
    "Container With Most Water": {
        "public":  [{"input": [1, 8, 6, 2, 5, 4, 8, 3, 7], "expected": 49}],
        "hidden":  [{"input": [1, 1], "expected": 1}, {"input": [4, 3, 2, 1, 4], "expected": 16}],
    },
    "Sort Colors": {
        "public":  [{"input": [2, 0, 2, 1, 1, 0], "expected": [0, 0, 1, 1, 2, 2]}],
        "hidden":  [{"input": [2, 0, 1], "expected": [0, 1, 2]}, {"input": [0], "expected": [0]}],
    },
    "Jump Game": {
        "public":  [{"input": [2, 3, 1, 1, 4], "expected": True}, {"input": [3, 2, 1, 0, 4], "expected": False}],
        "hidden":  [{"input": [0], "expected": True}],
    },
    "Anagram Check": {
        "public":  [{"input": ("listen", "silent"), "expected": True}, {"input": ("hello", "world"), "expected": False}],
        "hidden":  [{"input": ("", ""), "expected": True}],
    },
    "Subarray Sum Equals K": {
        "public":  [{"input": ([1, 1, 1], 2), "expected": 2}],
        "hidden":  [{"input": ([1, 2, 3], 3), "expected": 2}],
    },
    "Longest Palindromic Substring": {
        "public":  [{"input": "cbbd", "expected": "bb"}, {"input": "a", "expected": "a"}],
        "hidden":  [{"input": "racecar", "expected": "racecar"}],
    },

    # ── HARD ─────────────────────────────────────────────
    "Trapping Rain Water": {
        "public":  [{"input": [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], "expected": 6}],
        "hidden":  [{"input": [4, 2, 0, 3, 2, 5], "expected": 9}, {"input": [1, 0, 1], "expected": 1}],
    },
    "Median of Two Sorted Arrays": {
        "public":  [{"input": ([1, 3], [2]), "expected": 2.0}, {"input": ([1, 2], [3, 4]), "expected": 2.5}],
        "hidden":  [{"input": ([], [1]), "expected": 1.0}],
    },
    "Merge Intervals": {
        "public":  [{"input": [[1, 3], [2, 6], [8, 10]], "expected": [[1, 6], [8, 10]]}],
        "hidden":  [{"input": [[1, 4], [4, 5]], "expected": [[1, 5]]}, {"input": [[1, 4], [2, 3]], "expected": [[1, 4]]}],
    },
    "Minimum Window Substring": {
        "public":  [{"input": ("ADOBECODEBANC", "ABC"), "expected": "BANC"}],
        "hidden":  [{"input": ("a", "a"), "expected": "a"}, {"input": ("a", "aa"), "expected": ""}],
    },
    "N Queens": {
        "public":  [{"input": 4, "expected": 2}, {"input": 1, "expected": 1}],
        "hidden":  [{"input": 5, "expected": 10}, {"input": 6, "expected": 4}],
    },
    "Edit Distance": {
        "public":  [{"input": ("horse", "ros"), "expected": 3}],
        "hidden":  [{"input": ("intention", "execution"), "expected": 5}, {"input": ("abc", "abc"), "expected": 0}],
    },
    "Word Break": {
        "public":  [{"input": ("leetcode", ["leet", "code"]), "expected": True}],
        "hidden":  [{"input": ("catsandog", ["cats","dog","sand","cat","an"]), "expected": False}],
    },
    "Course Schedule": {
        "public":  [{"input": (2, [[1, 0]]), "expected": True}, {"input": (2, [[1, 0], [0, 1]]), "expected": False}],
        "hidden":  [{"input": (1, []), "expected": True}],
    },
    "Sliding Window Maximum": {
        "public":  [{"input": ([1, 3, -1, -3, 5, 3, 6, 7], 3), "expected": [3, 3, 5, 5, 6, 7]}],
        "hidden":  [{"input": ([1], 1), "expected": [1]}],
    },
    "Regular Expression Matching": {
        "public":  [{"input": ("aa", "a*"), "expected": True}, {"input": ("ab", ".*"), "expected": True}],
        "hidden":  [{"input": ("aab", "c*a*b"), "expected": True}],
    },
    "Palindrome Partitioning": {
        "public":  [{"input": "aab", "expected": 1}, {"input": "a", "expected": 0}],
        "hidden":  [{"input": "ab", "expected": 1}, {"input": "aaaa", "expected": 0}],
    },
    "Burst Balloons": {
        "public":  [{"input": [3, 1, 5, 8], "expected": 167}],
        "hidden":  [{"input": [1, 5], "expected": 10}, {"input": [5], "expected": 5}],
    },
    "Distinct Subsequences": {
        "public":  [{"input": ("rabbbit", "rabbit"), "expected": 3}],
        "hidden":  [{"input": ("babgbag", "bag"), "expected": 5}, {"input": ("a", "b"), "expected": 0}],
    },
    "Word Ladder": {
        "public":  [{"input": ("hit", "cog", ["hot","dot","dog","lot","log","cog"]), "expected": 5}],
        "hidden":  [{"input": ("hit", "cog", ["hot","dot","dog","lot","log"]), "expected": 0}],
    },
}


def _call(func, inp):
    """Call solution with correct argument unpacking."""
    if isinstance(inp, tuple):
        return func(*inp)
    return func(inp)


def run_tests(code: str, question):
    try:
        local_env = {}
        exec(compile(code, "<user_code>", "exec"), {}, local_env)

        if "solution" not in local_env:
            return {"error": "Define your function as 'def solution(...):' — the function must be named 'solution'."}

        func = local_env["solution"]
        q_title = question["title"]
        q_tests = TEST_CASES.get(q_title)

        if not q_tests:
            return {
                "error": f"No test cases defined for '{q_title}' yet.",
                "results": [], "passed": 0, "total": 0,
            }

        results = []
        passed = 0
        total = 0

        for visibility in ["public", "hidden"]:
            for test in q_tests.get(visibility, []):
                total += 1
                inp = test["input"]
                is_public = visibility == "public"

                try:
                    start = time.time()
                    output = _call(func, inp)
                    elapsed = time.time() - start

                    if elapsed > TIME_LIMIT:
                        results.append({
                            "input": str(inp) if is_public else None,
                            "expected": str(test["expected"]) if is_public else None,
                            "output": "Time Limit Exceeded",
                            "passed": False,
                            "type": visibility,
                        })
                        continue

                    is_pass = output == test["expected"]
                    if is_pass:
                        passed += 1

                    results.append({
                        "input": str(inp) if is_public else None,
                        "expected": str(test["expected"]) if is_public else None,
                        "output": str(output) if is_public else None,
                        "passed": is_pass,
                        "type": visibility,
                    })

                except Exception as e:
                    results.append({
                        "input": str(inp) if is_public else None,
                        "expected": str(test["expected"]) if is_public else None,
                        "output": str(e),
                        "passed": False,
                        "type": visibility,
                    })

        return {"results": results, "passed": passed, "total": total}

    except SyntaxError as e:
        return {"error": f"Syntax error: {e}"}
    except Exception:
        return {"error": traceback.format_exc()}