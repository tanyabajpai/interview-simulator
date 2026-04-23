import random

questions = {
    "easy": [
        {"title": "Palindrome Check", "description": "Check if string is palindrome."},
        {"title": "Reverse String", "description": "Reverse a string."},
        {"title": "Factorial", "description": "Calculate factorial of a number."},
    ],
    "medium": [
        {"title": "Two Sum", "description": "Find two numbers with target sum."},
        {"title": "Longest Substring", "description": "Without repeating characters."},
    ],
    "hard": [
        {"title": "LRU Cache", "description": "Design LRU cache."},
    ]
}

def get_random_question(difficulty: str):
    return random.choice(questions.get(difficulty, questions["easy"]))