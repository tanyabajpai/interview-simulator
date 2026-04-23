from db import questions_collection

questions = [
    {
        "title": "Fibonacci",
        "key": "fibonacci",
        "difficulty": "easy",
        "description": "Return nth Fibonacci number",
        "time": 600,
    },
    {
        "title": "Palindrome",
        "key": "palindrome",
        "difficulty": "easy",
        "description": "Check palindrome",
        "time": 600,
    },
    {
        "title": "Two Sum",
        "key": "two_sum",
        "difficulty": "medium",
        "description": "Find indices that sum to target",
        "time": 900,
    },
    {
        "title": "LRU Cache",
        "key": "lru",
        "difficulty": "hard",
        "description": "Design LRU cache",
        "time": 1200,
    }
]

questions_collection.delete_many({})
questions_collection.insert_many(questions)

print("✅ Questions seeded")