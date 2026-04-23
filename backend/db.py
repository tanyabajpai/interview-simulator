from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["interview_db"]

questions_collection = db["questions"]
attempts_collection = db["attempts"]