import random

QUESTION_BANK = {
    "easy": [
        {
            "title": "Reverse String",
            "description": "Given a string s, return the string reversed.\n\nExample:\n  Input: 'hello' → Output: 'olleh'\n  Input: 'abc'   → Output: 'cba'",
            "function_name": "solution",
            "test_cases": [
                {"input": "hello", "output": "olleh"},
                {"input": "abc", "output": "cba"},
                {"input": "", "output": ""},
                {"input": "a", "output": "a"},
            ],
        },
        {
            "title": "Palindrome Check",
            "description": "Return True if the string is a palindrome (reads the same forwards and backwards), else False.\n\nExample:\n  Input: 'racecar' → Output: True\n  Input: 'hello'   → Output: False",
            "function_name": "solution",
            "test_cases": [
                {"input": "racecar", "output": True},
                {"input": "hello", "output": False},
                {"input": "a", "output": True},
                {"input": "madam", "output": True},
            ],
        },
        {
            "title": "Factorial",
            "description": "Given a non-negative integer n, return n! (n factorial).\n\nExample:\n  Input: 5 → Output: 120\n  Input: 0 → Output: 1",
            "function_name": "solution",
            "test_cases": [
                {"input": 5, "output": 120},
                {"input": 0, "output": 1},
                {"input": 1, "output": 1},
                {"input": 7, "output": 5040},
            ],
        },
        {
            "title": "Fibonacci Number",
            "description": "Return the nth Fibonacci number (0-indexed). F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).\n\nExample:\n  Input: 6 → Output: 8\n  Input: 0 → Output: 0",
            "function_name": "solution",
            "test_cases": [
                {"input": 0, "output": 0},
                {"input": 1, "output": 1},
                {"input": 6, "output": 8},
                {"input": 10, "output": 55},
            ],
        },
        {
            "title": "Count Vowels",
            "description": "Count the number of vowels (a, e, i, o, u — case-insensitive) in the given string.\n\nExample:\n  Input: 'hello' → Output: 2\n  Input: 'rhythm' → Output: 0",
            "function_name": "solution",
            "test_cases": [
                {"input": "hello", "output": 2},
                {"input": "rhythm", "output": 0},
                {"input": "AEIOUaeiou", "output": 10},
                {"input": "", "output": 0},
            ],
        },
        {
            "title": "Sum of List",
            "description": "Given a list of integers, return their sum.\n\nExample:\n  Input: [1, 2, 3, 4] → Output: 10\n  Input: []           → Output: 0",
            "function_name": "solution",
            "test_cases": [
                {"input": [1, 2, 3, 4], "output": 10},
                {"input": [], "output": 0},
                {"input": [-1, 1], "output": 0},
                {"input": [100], "output": 100},
            ],
        },
        {
            "title": "Check Prime",
            "description": "Return True if the number is prime, else False. A prime number is greater than 1 and divisible only by 1 and itself.\n\nExample:\n  Input: 7  → Output: True\n  Input: 10 → Output: False",
            "function_name": "solution",
            "test_cases": [
                {"input": 7, "output": True},
                {"input": 10, "output": False},
                {"input": 2, "output": True},
                {"input": 1, "output": False},
            ],
        },
        {
            "title": "Max in List",
            "description": "Given a non-empty list of integers, return the maximum element without using Python's built-in max().\n\nExample:\n  Input: [3, 1, 4, 1, 5, 9] → Output: 9",
            "function_name": "solution",
            "test_cases": [
                {"input": [3, 1, 4, 1, 5, 9], "output": 9},
                {"input": [-1, -5, -2], "output": -1},
                {"input": [42], "output": 42},
                {"input": [0, 0, 0], "output": 0},
            ],
        },
        {
            "title": "Count Words",
            "description": "Given a string, return the number of words. Words are separated by spaces.\n\nExample:\n  Input: 'hello world' → Output: 2\n  Input: ''            → Output: 0",
            "function_name": "solution",
            "test_cases": [
                {"input": "hello world", "output": 2},
                {"input": "", "output": 0},
                {"input": "one", "output": 1},
                {"input": "a b c d e", "output": 5},
            ],
        },
        {
            "title": "Remove Duplicates",
            "description": "Given a list, return a new list with duplicates removed, preserving the original order.\n\nExample:\n  Input: [1,2,2,3,3,3] → Output: [1,2,3]\n  Input: [5,5,5]       → Output: [5]",
            "function_name": "solution",
            "test_cases": [
                {"input": [1, 2, 2, 3, 3, 3], "output": [1, 2, 3]},
                {"input": [5, 5, 5], "output": [5]},
                {"input": [], "output": []},
                {"input": [1, 2, 3], "output": [1, 2, 3]},
            ],
        },
        {
            "title": "FizzBuzz",
            "description": "Given an integer n, return a list of strings 1 to n where:\n  - multiples of 3 → 'Fizz'\n  - multiples of 5 → 'Buzz'\n  - multiples of both → 'FizzBuzz'\n  - otherwise → the number as a string\n\nExample:\n  Input: 5 → Output: ['1','2','Fizz','4','Buzz']",
            "function_name": "solution",
            "test_cases": [
                {"input": 5, "output": ["1","2","Fizz","4","Buzz"]},
                {"input": 15, "output": ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]},
                {"input": 1, "output": ["1"]},
            ],
        },
        {
            "title": "Sum of Digits",
            "description": "Given a non-negative integer, return the sum of its digits.\n\nExample:\n  Input: 1234 → Output: 10\n  Input: 9    → Output: 9",
            "function_name": "solution",
            "test_cases": [
                {"input": 1234, "output": 10},
                {"input": 9, "output": 9},
                {"input": 0, "output": 0},
                {"input": 999, "output": 27},
            ],
        },
        {
            "title": "Uppercase String",
            "description": "Convert the given string to uppercase without using Python's .upper() method.\n\nExample:\n  Input: 'hello' → Output: 'HELLO'",
            "function_name": "solution",
            "test_cases": [
                {"input": "hello", "output": "HELLO"},
                {"input": "Hello World", "output": "HELLO WORLD"},
                {"input": "", "output": ""},
                {"input": "abc123", "output": "ABC123"},
            ],
        },
        {
            "title": "Average of List",
            "description": "Given a non-empty list of numbers, return the average rounded to 2 decimal places.\n\nExample:\n  Input: [1, 2, 3, 4, 5] → Output: 3.0\n  Input: [1, 2]          → Output: 1.5",
            "function_name": "solution",
            "test_cases": [
                {"input": [1, 2, 3, 4, 5], "output": 3.0},
                {"input": [1, 2], "output": 1.5},
                {"input": [10], "output": 10.0},
                {"input": [1, 1, 1, 1], "output": 1.0},
            ],
        },
        {
            "title": "Flatten List",
            "description": "Given a list of lists (one level deep), return a single flat list.\n\nExample:\n  Input: [[1,2],[3,4],[5]] → Output: [1,2,3,4,5]",
            "function_name": "solution",
            "test_cases": [
                {"input": [[1, 2], [3, 4], [5]], "output": [1, 2, 3, 4, 5]},
                {"input": [[], [1], [2, 3]], "output": [1, 2, 3]},
                {"input": [[]], "output": []},
                {"input": [[1, 2, 3]], "output": [1, 2, 3]},
            ],
        },
        {
            "title": "Count Occurrences",
            "description": "Given a list and a value, return the number of times the value appears in the list — without using list.count().\n\nExample:\n  Input: ([1,2,2,3,2], 2) → Output: 3",
            "function_name": "solution",
            "test_cases": [
                {"input": [[1, 2, 2, 3, 2], 2], "output": 3},
                {"input": [[1, 2, 3], 5], "output": 0},
                {"input": [[], 1], "output": 0},
                {"input": [["a","b","a"], "a"], "output": 2},
            ],
        },
        {
            "title": "Power Function",
            "description": "Given a base and exponent (both non-negative integers), return base raised to the power exponent without using ** or pow().\n\nExample:\n  Input: (2, 10) → Output: 1024",
            "function_name": "solution",
            "test_cases": [
                {"input": [2, 10], "output": 1024},
                {"input": [3, 3], "output": 27},
                {"input": [5, 0], "output": 1},
                {"input": [1, 100], "output": 1},
            ],
        },
        {
            "title": "Merge Two Sorted Lists",
            "description": "Given two sorted lists of integers, return a single sorted merged list.\n\nExample:\n  Input: ([1,3,5], [2,4,6]) → Output: [1,2,3,4,5,6]",
            "function_name": "solution",
            "test_cases": [
                {"input": [[1, 3, 5], [2, 4, 6]], "output": [1, 2, 3, 4, 5, 6]},
                {"input": [[], [1, 2]], "output": [1, 2]},
                {"input": [[1], []], "output": [1]},
                {"input": [[1, 2], [1, 2]], "output": [1, 1, 2, 2]},
            ],
        },
        {
            "title": "Missing Number",
            "description": "Given a list containing n distinct numbers in range [0, n], return the one missing number.\n\nExample:\n  Input: [3,0,1] → Output: 2\n  Input: [0,1]   → Output: 2",
            "function_name": "solution",
            "test_cases": [
                {"input": [3, 0, 1], "output": 2},
                {"input": [0, 1], "output": 2},
                {"input": [0], "output": 1},
                {"input": [1], "output": 0},
            ],
        },
        {
            "title": "Is Anagram",
            "description": "Given two strings, return True if they are anagrams of each other (same characters, same frequency, case-insensitive), else False.\n\nExample:\n  Input: ('listen', 'silent') → Output: True\n  Input: ('hello', 'world')   → Output: False",
            "function_name": "solution",
            "test_cases": [
                {"input": ["listen", "silent"], "output": True},
                {"input": ["hello", "world"], "output": False},
                {"input": ["Astronomer", "Moon starer"], "output": False},
                {"input": ["abc", "cab"], "output": True},
            ],
        },
    ],

    "medium": [
        {
            "title": "Two Sum",
            "description": "Given a list of integers and a target, return the indices of the two numbers that add up to the target. Each input has exactly one solution.\n\nExample:\n  Input: ([2,7,11,15], 9) → Output: [0,1]",
            "function_name": "solution",
            "test_cases": [
                {"input": [[2, 7, 11, 15], 9], "output": [0, 1]},
                {"input": [[3, 2, 4], 6], "output": [1, 2]},
                {"input": [[3, 3], 6], "output": [0, 1]},
            ],
        },
        {
            "title": "Valid Parentheses",
            "description": "Given a string containing '(', ')', '{', '}', '[' and ']', return True if the string is valid — every open bracket is closed in the correct order.\n\nExample:\n  Input: '()[]{}' → Output: True\n  Input: '(]'     → Output: False",
            "function_name": "solution",
            "test_cases": [
                {"input": "()[]{}", "output": True},
                {"input": "(]", "output": False},
                {"input": "{[]}", "output": True},
                {"input": "((", "output": False},
            ],
        },
        {
            "title": "Longest Substring Without Repeating",
            "description": "Given a string, find the length of the longest substring without repeating characters.\n\nExample:\n  Input: 'abcabcbb' → Output: 3 (abc)\n  Input: 'bbbbb'    → Output: 1",
            "function_name": "solution",
            "test_cases": [
                {"input": "abcabcbb", "output": 3},
                {"input": "bbbbb", "output": 1},
                {"input": "pwwkew", "output": 3},
                {"input": "", "output": 0},
            ],
        },
        {
            "title": "Second Largest",
            "description": "Given a list of integers, return the second largest distinct element. Return -1 if it doesn't exist.\n\nExample:\n  Input: [3,1,4,1,5,9,2,6] → Output: 6",
            "function_name": "solution",
            "test_cases": [
                {"input": [3, 1, 4, 1, 5, 9, 2, 6], "output": 6},
                {"input": [1, 1], "output": -1},
                {"input": [5, 3], "output": 3},
                {"input": [1], "output": -1},
            ],
        },
        {
            "title": "Rotate Array",
            "description": "Given a list of integers and k, rotate the array to the right by k steps.\n\nExample:\n  Input: ([1,2,3,4,5,6,7], 3) → Output: [5,6,7,1,2,3,4]",
            "function_name": "solution",
            "test_cases": [
                {"input": [[1, 2, 3, 4, 5, 6, 7], 3], "output": [5, 6, 7, 1, 2, 3, 4]},
                {"input": [[-1, -100, 3, 99], 2], "output": [3, 99, -1, -100]},
                {"input": [[1, 2], 3], "output": [2, 1]},
            ],
        },
        {
            "title": "Product Except Self",
            "description": "Given a list of integers, return a list where each element is the product of all other elements. Do not use division.\n\nExample:\n  Input: [1,2,3,4] → Output: [24,12,8,6]",
            "function_name": "solution",
            "test_cases": [
                {"input": [1, 2, 3, 4], "output": [24, 12, 8, 6]},
                {"input": [-1, 1, 0, -3, 3], "output": [0, 0, 9, 0, 0]},
                {"input": [2, 3], "output": [3, 2]},
            ],
        },
        {
            "title": "Group Anagrams",
            "description": "Given a list of strings, group the anagrams together. Return a list of groups (order within groups doesn't matter).\n\nExample:\n  Input: ['eat','tea','tan','ate','nat','bat']\n  Output: [['eat','tea','ate'],['tan','nat'],['bat']]",
            "function_name": "solution",
            "test_cases": [
                {"input": [["eat","tea","tan","ate","nat","bat"]], "output": [["ate","eat","tea"],["nat","tan"],["bat"]]},
                {"input": [[""]], "output": [[""]]},
                {"input": [["a"]], "output": [["a"]]},
            ],
        },
        {
            "title": "Top K Frequent Elements",
            "description": "Given a list of integers and k, return the k most frequent elements.\n\nExample:\n  Input: ([1,1,1,2,2,3], 2) → Output: [1,2]",
            "function_name": "solution",
            "test_cases": [
                {"input": [[1, 1, 1, 2, 2, 3], 2], "output": [1, 2]},
                {"input": [[1], 1], "output": [1]},
                {"input": [[4, 4, 4, 5, 5, 6], 2], "output": [4, 5]},
            ],
        },
        {
            "title": "Kth Largest Element",
            "description": "Find the kth largest element in a list. It is the kth largest in sorted order, not the kth distinct.\n\nExample:\n  Input: ([3,2,1,5,6,4], 2) → Output: 5",
            "function_name": "solution",
            "test_cases": [
                {"input": [[3, 2, 1, 5, 6, 4], 2], "output": 5},
                {"input": [[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], "output": 4},
                {"input": [[1], 1], "output": 1},
            ],
        },
        {
            "title": "Container With Most Water",
            "description": "Given a list of heights representing vertical lines, find two lines that together with the x-axis form a container with the most water. Return the maximum area.\n\nExample:\n  Input: [1,8,6,2,5,4,8,3,7] → Output: 49",
            "function_name": "solution",
            "test_cases": [
                {"input": [1, 8, 6, 2, 5, 4, 8, 3, 7], "output": 49},
                {"input": [1, 1], "output": 1},
                {"input": [4, 3, 2, 1, 4], "output": 16},
            ],
        },
        {
            "title": "Longest Palindromic Substring",
            "description": "Given a string, return the longest palindromic substring.\n\nExample:\n  Input: 'babad' → Output: 'bab' (or 'aba')\n  Input: 'cbbd'  → Output: 'bb'",
            "function_name": "solution",
            "test_cases": [
                {"input": "cbbd", "output": "bb"},
                {"input": "a", "output": "a"},
                {"input": "racecar", "output": "racecar"},
            ],
        },
        {
            "title": "Subarray Sum Equals K",
            "description": "Given a list of integers and k, return the total number of contiguous subarrays whose sum equals k.\n\nExample:\n  Input: ([1,1,1], 2) → Output: 2",
            "function_name": "solution",
            "test_cases": [
                {"input": [[1, 1, 1], 2], "output": 2},
                {"input": [[1, 2, 3], 3], "output": 2},
                {"input": [[0, 0, 0], 0], "output": 6},
            ],
        },
        {
            "title": "Sort Colors",
            "description": "Given a list with values 0, 1, and 2 (Dutch National Flag), sort it in-place so all 0s come first, then 1s, then 2s.\n\nExample:\n  Input: [2,0,2,1,1,0] → Output: [0,0,1,1,2,2]",
            "function_name": "solution",
            "test_cases": [
                {"input": [2, 0, 2, 1, 1, 0], "output": [0, 0, 1, 1, 2, 2]},
                {"input": [2, 0, 1], "output": [0, 1, 2]},
                {"input": [0], "output": [0]},
            ],
        },
        {
            "title": "Spiral Matrix",
            "description": "Given an m x n matrix, return all elements in spiral order.\n\nExample:\n  Input: [[1,2,3],[4,5,6],[7,8,9]]\n  Output: [1,2,3,6,9,8,7,4,5]",
            "function_name": "solution",
            "test_cases": [
                {"input": [[[1,2,3],[4,5,6],[7,8,9]]], "output": [1,2,3,6,9,8,7,4,5]},
                {"input": [[[1,2],[3,4]]], "output": [1,2,4,3]},
                {"input": [[[3],[2]]], "output": [3, 2]},
            ],
        },
        {
            "title": "Combination Sum",
            "description": "Given a list of distinct integers (candidates) and a target, return all unique combinations where candidates sum to target. The same number may be used multiple times.\n\nExample:\n  Input: ([2,3,6,7], 7) → Output: [[2,2,3],[7]]",
            "function_name": "solution",
            "test_cases": [
                {"input": [[2, 3, 6, 7], 7], "output": [[2, 2, 3], [7]]},
                {"input": [[2, 3, 5], 8], "output": [[2, 2, 2, 2], [2, 3, 3], [3, 5]]},
                {"input": [[2], 1], "output": []},
            ],
        },
        {
            "title": "Permutations",
            "description": "Given a list of distinct integers, return all possible permutations.\n\nExample:\n  Input: [1,2,3]\n  Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]",
            "function_name": "solution",
            "test_cases": [
                {"input": [[1, 2, 3]], "output": [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]},
                {"input": [[1]], "output": [[1]]},
                {"input": [[0, 1]], "output": [[0,1],[1,0]]},
            ],
        },
        {
            "title": "Search in Rotated Sorted Array",
            "description": "Given a rotated sorted array and a target, return the index of the target or -1 if not found.\n\nExample:\n  Input: ([4,5,6,7,0,1,2], 0) → Output: 4",
            "function_name": "solution",
            "test_cases": [
                {"input": [[4, 5, 6, 7, 0, 1, 2], 0], "output": 4},
                {"input": [[4, 5, 6, 7, 0, 1, 2], 3], "output": -1},
                {"input": [[1], 0], "output": -1},
            ],
        },
        {
            "title": "Word Search",
            "description": "Given a 2D board of characters and a word, return True if the word exists in the grid. The word can be constructed from sequentially adjacent cells (horizontally or vertically).\n\nExample:\n  Input: board=[['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word='ABCCED' → True",
            "function_name": "solution",
            "test_cases": [
                {"input": [[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED"], "output": True},
                {"input": [[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "SEE"], "output": True},
                {"input": [[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCB"], "output": False},
            ],
        },
        {
            "title": "Set Matrix Zeroes",
            "description": "Given an m x n matrix, if an element is 0, set its entire row and column to 0 in-place. Return the modified matrix.\n\nExample:\n  Input: [[1,1,1],[1,0,1],[1,1,1]] → Output: [[1,0,1],[0,0,0],[1,0,1]]",
            "function_name": "solution",
            "test_cases": [
                {"input": [[[1,1,1],[1,0,1],[1,1,1]]], "output": [[1,0,1],[0,0,0],[1,0,1]]},
                {"input": [[[0,1,2,0],[3,4,5,2],[1,3,1,5]]], "output": [[0,0,0,0],[3,4,5,0],[1,3,1,0]]},
            ],
        },
        {
            "title": "Jump Game",
            "description": "Given a list of non-negative integers where each element is the max jump length from that position, return True if you can reach the last index starting from index 0.\n\nExample:\n  Input: [2,3,1,1,4] → Output: True\n  Input: [3,2,1,0,4] → Output: False",
            "function_name": "solution",
            "test_cases": [
                {"input": [2, 3, 1, 1, 4], "output": True},
                {"input": [3, 2, 1, 0, 4], "output": False},
                {"input": [0], "output": True},
                {"input": [1, 0, 1], "output": False},
            ],
        },
    ],

    "hard": [
        {
            "title": "Trapping Rain Water",
            "description": "Given a list of non-negative integers representing an elevation map where the width of each bar is 1, compute how much water can be trapped after raining.\n\nExample:\n  Input: [0,1,0,2,1,0,1,3,2,1,2,1] → Output: 6",
            "function_name": "solution",
            "test_cases": [
                {"input": [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], "output": 6},
                {"input": [4, 2, 0, 3, 2, 5], "output": 9},
                {"input": [1, 0, 1], "output": 1},
                {"input": [3, 0, 0, 2, 0, 4], "output": 10},
            ],
        },
        {
            "title": "Median of Two Sorted Arrays",
            "description": "Given two sorted arrays, return the median of the two arrays combined. The overall run time complexity should be O(log(m+n)).\n\nExample:\n  Input: ([1,3], [2]) → Output: 2.0\n  Input: ([1,2], [3,4]) → Output: 2.5",
            "function_name": "solution",
            "test_cases": [
                {"input": [[1, 3], [2]], "output": 2.0},
                {"input": [[1, 2], [3, 4]], "output": 2.5},
                {"input": [[0, 0], [0, 0]], "output": 0.0},
                {"input": [[], [1]], "output": 1.0},
            ],
        },
        {
            "title": "LRU Cache",
            "description": "Design a data structure that follows Least Recently Used (LRU) cache constraints. Implement the LRUCache class:\n  - LRUCache(capacity): initialize with positive capacity\n  - get(key): return value if exists, else -1\n  - put(key, value): update or insert; evict LRU when over capacity\n\nReturn results of operations given as a list.",
            "function_name": "solution",
            "test_cases": [
                {"input": [[["LRUCache","put","put","get","put","get","put","get","get","get"],[2,[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]]],
                 "output": [None,None,None,1,None,-1,None,-1,3,4]},
            ],
        },
        {
            "title": "Merge Intervals",
            "description": "Given a list of intervals [start, end], merge all overlapping intervals and return the result.\n\nExample:\n  Input: [[1,3],[2,6],[8,10],[15,18]] → Output: [[1,6],[8,10],[15,18]]",
            "function_name": "solution",
            "test_cases": [
                {"input": [[[1,3],[2,6],[8,10],[15,18]]], "output": [[1,6],[8,10],[15,18]]},
                {"input": [[[1,4],[4,5]]], "output": [[1,5]]},
                {"input": [[[1,4],[2,3]]], "output": [[1,4]]},
            ],
        },
        {
            "title": "Minimum Window Substring",
            "description": "Given strings s and t, return the minimum window substring of s that contains all characters of t. Return '' if no such window exists.\n\nExample:\n  Input: ('ADOBECODEBANC', 'ABC') → Output: 'BANC'",
            "function_name": "solution",
            "test_cases": [
                {"input": ["ADOBECODEBANC", "ABC"], "output": "BANC"},
                {"input": ["a", "a"], "output": "a"},
                {"input": ["a", "aa"], "output": ""},
            ],
        },
        {
            "title": "N Queens",
            "description": "Return the number of distinct solutions to the N-Queens puzzle for a given n.\n\nExample:\n  Input: 4 → Output: 2\n  Input: 1 → Output: 1",
            "function_name": "solution",
            "test_cases": [
                {"input": 4, "output": 2},
                {"input": 1, "output": 1},
                {"input": 5, "output": 10},
                {"input": 6, "output": 4},
            ],
        },
        {
            "title": "Edit Distance",
            "description": "Given two strings word1 and word2, return the minimum number of operations (insert, delete, replace) to convert word1 to word2.\n\nExample:\n  Input: ('horse', 'ros') → Output: 3",
            "function_name": "solution",
            "test_cases": [
                {"input": ["horse", "ros"], "output": 3},
                {"input": ["intention", "execution"], "output": 5},
                {"input": ["", "a"], "output": 1},
                {"input": ["abc", "abc"], "output": 0},
            ],
        },
        {
            "title": "Word Break",
            "description": "Given a string s and a list of words (wordDict), return True if s can be segmented into a space-separated sequence of one or more dictionary words.\n\nExample:\n  Input: ('leetcode', ['leet','code']) → True\n  Input: ('catsandog', ['cats','dog','sand','cat','an']) → False",
            "function_name": "solution",
            "test_cases": [
                {"input": ["leetcode", ["leet", "code"]], "output": True},
                {"input": ["applepenapple", ["apple", "pen"]], "output": True},
                {"input": ["catsandog", ["cats","dog","sand","cat","an"]], "output": False},
            ],
        },
        {
            "title": "Course Schedule",
            "description": "There are numCourses courses. Given a list of [course, prerequisite] pairs, return True if it's possible to finish all courses (i.e., no cycle exists).\n\nExample:\n  Input: (2, [[1,0]]) → True\n  Input: (2, [[1,0],[0,1]]) → False",
            "function_name": "solution",
            "test_cases": [
                {"input": [2, [[1, 0]]], "output": True},
                {"input": [2, [[1, 0], [0, 1]]], "output": False},
                {"input": [1, []], "output": True},
                {"input": [4, [[1,0],[2,0],[3,1],[3,2]]], "output": True},
            ],
        },
        {
            "title": "Sliding Window Maximum",
            "description": "Given an integer array and a sliding window of size k, return the maximum of each window as it slides from left to right.\n\nExample:\n  Input: ([1,3,-1,-3,5,3,6,7], 3) → Output: [3,3,5,5,6,7]",
            "function_name": "solution",
            "test_cases": [
                {"input": [[1, 3, -1, -3, 5, 3, 6, 7], 3], "output": [3, 3, 5, 5, 6, 7]},
                {"input": [[1], 1], "output": [1]},
                {"input": [[9, 11], 2], "output": [11]},
            ],
        },
        {
            "title": "Regular Expression Matching",
            "description": "Implement regular expression matching supporting '.' (matches any single character) and '*' (matches zero or more of the preceding element). The match must cover the entire string.\n\nExample:\n  Input: ('aa', 'a*') → True\n  Input: ('ab', '.*') → True",
            "function_name": "solution",
            "test_cases": [
                {"input": ["aa", "a*"], "output": True},
                {"input": ["ab", ".*"], "output": True},
                {"input": ["aab", "c*a*b"], "output": True},
                {"input": ["mississippi", "mis*is*p*."], "output": False},
            ],
        },
        {
            "title": "Palindrome Partitioning",
            "description": "Given a string s, return the minimum number of cuts needed to partition it such that every substring is a palindrome.\n\nExample:\n  Input: 'aab' → Output: 1 (cut between 'aa' and 'b')\n  Input: 'a'   → Output: 0",
            "function_name": "solution",
            "test_cases": [
                {"input": "aab", "output": 1},
                {"input": "a", "output": 0},
                {"input": "ab", "output": 1},
                {"input": "aaaa", "output": 0},
            ],
        },
        {
            "title": "Maximal Rectangle",
            "description": "Given a binary matrix (0s and 1s), return the area of the largest rectangle containing only 1s.\n\nExample:\n  Input: [['1','0','1','0','0'],['1','0','1','1','1'],['1','1','1','1','1'],['1','0','0','1','0']]\n  Output: 6",
            "function_name": "solution",
            "test_cases": [
                {"input": [[["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]], "output": 6},
                {"input": [[["0"]]], "output": 0},
                {"input": [[["1"]]], "output": 1},
            ],
        },
        {
            "title": "Serialize and Deserialize Binary Tree",
            "description": "Design an algorithm to serialize a binary tree to a string and deserialize it back. Use a simple representation: [1,2,3,null,null,4,5]. Return the deserialized tree root's level-order traversal to verify correctness.",
            "function_name": "solution",
            "test_cases": [
                {"input": [[1, 2, 3, None, None, 4, 5]], "output": [1, 2, 3, None, None, 4, 5]},
                {"input": [[]], "output": []},
            ],
        },
        {
            "title": "Alien Dictionary",
            "description": "Given a sorted list of words from an alien language, determine the order of characters in the alien alphabet. Return the characters in order, or '' if invalid.\n\nExample:\n  Input: ['wrt','wrf','er','ett','rftt'] → Output: 'wertf'",
            "function_name": "solution",
            "test_cases": [
                {"input": [["wrt","wrf","er","ett","rftt"]], "output": "wertf"},
                {"input": [["z","x"]], "output": "zx"},
                {"input": [["z","x","z"]], "output": ""},
            ],
        },
        {
            "title": "Burst Balloons",
            "description": "Given n balloons with numbers on them, you can burst them one by one. If you burst balloon i (with neighbors left l and right r), you earn nums[l]*nums[i]*nums[r] coins. Maximize total coins.\n\nExample:\n  Input: [3,1,5,8] → Output: 167",
            "function_name": "solution",
            "test_cases": [
                {"input": [[3, 1, 5, 8]], "output": 167},
                {"input": [[1, 5]], "output": 10},
                {"input": [[5]], "output": 5},
            ],
        },
        {
            "title": "Distinct Subsequences",
            "description": "Given strings s and t, return the number of distinct subsequences of s which equals t.\n\nExample:\n  Input: ('rabbbit', 'rabbit') → Output: 3",
            "function_name": "solution",
            "test_cases": [
                {"input": ["rabbbit", "rabbit"], "output": 3},
                {"input": ["babgbag", "bag"], "output": 5},
                {"input": ["a", "b"], "output": 0},
            ],
        },
        {
            "title": "Sudoku Solver",
            "description": "Solve a 9x9 Sudoku puzzle in-place.",
            "function_name": "solution",
            "test_cases": [
                {
                     "input": [[
                         ["5","3",".",".","7",".",".",".","."],
                         ["6",".",".","1","9","5",".",".","."],
                         [".","9","8",".",".",".",".","6","."],
                         ["8",".",".",".","6",".",".",".","3"],
                         ["4",".",".","8",".","3",".",".","1"],
                         ["7",".",".",".","2",".",".",".","6"],
                         [".","6",".",".",".",".","2","8","."],
                         [".",".",".","4","1","9",".",".","5"],
                         [".",".",".",".","8",".",".","7","9"]
                    ]],
                     "output": [[
                         ["5","3","4","6","7","8","9","1","2"],
                         ["6","7","2","1","9","5","3","4","8"],
                         ["1","9","8","3","4","2","5","6","7"],
                         ["8","5","9","7","6","1","4","2","3"],
                         ["4","2","6","8","5","3","7","9","1"],
                         ["7","1","3","9","2","4","8","5","6"],
                         ["9","6","1","5","3","7","2","8","4"],
                         ["2","8","7","4","1","9","6","3","5"],
                         ["3","4","5","2","8","6","1","7","9"]
                    ]]
                }
            ],
        },
        {
            "title": "Word Ladder",
            "description": "Given beginWord, endWord, and a wordList, return the number of words in the shortest transformation sequence from beginWord to endWord (changing one letter at a time, each intermediate word must be in wordList). Return 0 if no such sequence exists.\n\nExample:\n  Input: ('hit','cog',['hot','dot','dog','lot','log','cog']) → Output: 5",
            "function_name": "solution",
            "test_cases": [
                {"input": ["hit", "cog", ["hot","dot","dog","lot","log","cog"]], "output": 5},
                {"input": ["hit", "cog", ["hot","dot","dog","lot","log"]], "output": 0},
            ],
        },
    ],
}

# =========================
# NO-REPEAT SYSTEM
# =========================
used_questions = {"easy": [], "medium": [], "hard": []}


def get_random_question(difficulty: str):
    difficulty = difficulty.lower()
    pool = QUESTION_BANK.get(difficulty, [])
    if not pool:
        return {"title": "No Questions", "description": "Add questions to the bank."}
    if len(used_questions[difficulty]) >= len(pool):
        used_questions[difficulty] = []
    available = [q for q in pool if q["title"] not in [u["title"] for u in used_questions[difficulty]]]
    q = random.choice(available)
    used_questions[difficulty].append(q)
    return q