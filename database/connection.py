import os
from functools import lru_cache
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


@lru_cache(maxsize=1)
def get_database():
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise RuntimeError("MONGODB_URI is not configured")
    client = MongoClient(uri, serverSelectionTimeoutMS=30000)
    client.admin.command("ping")
    return client[os.getenv("DATABASE_NAME", "learnwise_ai")]


def create_indexes(db):
    db.users.create_index("email", unique=True)
    db.auth_sessions.create_index("token_hash", unique=True)
    db.auth_sessions.create_index("expires_at", expireAfterSeconds=0)
    db.student_profiles.create_index("user_id")
    db.tutor_conversations.create_index("user_id")
    db.assessments.create_index([("user_id", 1), ("created_at", -1)])
    db.quiz_attempts.create_index([("user_id", 1), ("created_at", -1)])
    db.topic_progress.create_index([("user_id", 1), ("subject", 1), ("topic", 1)], unique=True)
