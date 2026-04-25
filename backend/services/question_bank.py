import random

# =========================
# ✅ REAL QUESTIONS (CLEAN)
# =========================

QUESTION_BANK = {
    "easy": [
        {
    "title": "Reverse String",
    "description": "Reverse a string.",
    "function_name": "solution",
    "test_cases": [
        {"input": "hello", "output": "olleh"},
        {"input": "abc", "output": "cba"},
        {"input": "", "output": ""},
        {"input": "a", "output": "a"}
    ]
},
        {"title": "Palindrome Check", "description": "Check if string is palindrome."},
        {"title": "Factorial", "description": "Calculate factorial of a number."},
        {"title": "Fibonacci Number", "description": "Return nth Fibonacci number."},
        {"title": "Sum of Digits", "description": "Find sum of digits."},
        {"title": "Count Vowels", "description": "Count vowels in string."},
        {"title": "Max in List", "description": "Find maximum element."},
        {"title": "Min in List", "description": "Find minimum element."},
        {"title": "Even or Odd", "description": "Check if number is even or odd."},
        {"title": "Remove Spaces", "description": "Remove spaces from string."},
        {"title": "Count Words", "description": "Count words in string."},
        {"title": "Square Number", "description": "Return square of a number."},
        {"title": "Cube Number", "description": "Return cube of a number."},
        {"title": "Check Prime", "description": "Check if number is prime."},
        {"title": "Find Length", "description": "Find length of string."},
        {"title": "Uppercase String", "description": "Convert string to uppercase."},
        {"title": "Lowercase String", "description": "Convert string to lowercase."},
        {"title": "Sum of List", "description": "Find sum of list elements."},
        {"title": "Average of List", "description": "Find average of list."},
        {"title": "Find Index", "description": "Find index of element."},
    ],

    "medium": [
        {"title": "Two Sum", "description": "Find two numbers with target sum."},
        {"title": "Anagram Check", "description": "Check if strings are anagrams."},
        {"title": "Second Largest", "description": "Find second largest element."},
        {"title": "Rotate Array", "description": "Rotate array by k steps."},
        {"title": "Longest Substring", "description": "Longest substring without repeat."},
        {"title": "Subarray Sum", "description": "Find subarray with given sum."},
        {"title": "Group Anagrams", "description": "Group anagrams."},
        {"title": "Valid Parentheses", "description": "Check valid parentheses."},
        {"title": "Product Except Self", "description": "Return product of array except self."},
        {"title": "Sort Colors", "description": "Sort array of 0s,1s,2s."},
        {"title": "Search Rotated Array", "description": "Search in rotated sorted array."},
        {"title": "Container With Most Water", "description": "Find max water container."},
        {"title": "Longest Palindromic Substring", "description": "Find longest palindrome substring."},
        {"title": "Spiral Matrix", "description": "Return matrix in spiral order."},
        {"title": "Set Matrix Zeroes", "description": "Set rows/cols to zero."},
        {"title": "Word Search", "description": "Search word in grid."},
        {"title": "Combination Sum", "description": "Find combinations that sum to target."},
        {"title": "Permutations", "description": "Generate all permutations."},
        {"title": "Kth Largest Element", "description": "Find kth largest element."},
        {"title": "Top K Frequent Elements", "description": "Find top k frequent elements."},
    ],

    "hard": [
        {"title": "LRU Cache", "description": "Design LRU cache."},
        {"title": "Merge Intervals", "description": "Merge overlapping intervals."},
        {"title": "Word Ladder", "description": "Transform words."},
        {"title": "N Queens", "description": "Solve N queens problem."},
        {"title": "Trapping Rain Water", "description": "Calculate trapped water."},
        {"title": "Median of Two Arrays", "description": "Find median of two sorted arrays."},
        {"title": "Sliding Window Maximum", "description": "Find max in sliding window."},
        {"title": "Serialize Binary Tree", "description": "Serialize and deserialize tree."},
        {"title": "Edit Distance", "description": "Compute minimum edit distance."},
        {"title": "Minimum Window Substring", "description": "Find smallest substring containing all chars."},
        {"title": "Word Break II", "description": "Break string into valid sentences."},
        {"title": "Alien Dictionary", "description": "Determine character order."},
        {"title": "Course Schedule II", "description": "Find order of courses."},
        {"title": "Maximal Rectangle", "description": "Largest rectangle in matrix."},
        {"title": "Burst Balloons", "description": "Max coins problem."},
        {"title": "Regular Expression Matching", "description": "Implement regex matching."},
        {"title": "Sudoku Solver", "description": "Solve Sudoku puzzle."},
        {"title": "Distinct Subsequences", "description": "Count distinct subsequences."},
        {"title": "Palindrome Partitioning II", "description": "Min cuts for palindrome partition."},
        {"title": "Max Points on Line", "description": "Find max collinear points."},
    ],
}

# =========================
# 🚫 NO REPEAT SYSTEM
# =========================

used_questions = {
    "easy": [],
    "medium": [],
    "hard": [],
}


def get_random_question(difficulty: str):
    difficulty = difficulty.lower()
    pool = QUESTION_BANK.get(difficulty, [])

    if not pool:
        return {"title": "No Questions", "description": "Add questions"}

    # 🔥 Reset when exhausted
    if len(used_questions[difficulty]) == len(pool):
        used_questions[difficulty] = []

    available = [
        q for q in pool
        if q not in used_questions[difficulty]
    ]

    q = random.choice(available)
    used_questions[difficulty].append(q)

    return q