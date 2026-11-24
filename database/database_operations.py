from datetime import datetime, timezone
from bson import ObjectId
from database.connection import get_database


def utcnow():
    return datetime.now(timezone.utc)


def _db():
    return get_database()


def create_user(full_name, email, password_hash):
    result = _db().users.insert_one({
        "full_name": full_name, "email": email.lower().strip(),
        "password_hash": password_hash, "created_at": utcnow(), "is_active": True
    })
    return str(result.inserted_id)


def find_user_by_email(email):
    return _db().users.find_one({"email": email.lower().strip()})


def find_user_by_id(user_id):
    return _db().users.find_one({"_id": ObjectId(user_id)})


def save_profile(user_id, profile):
    profile = {**profile, "user_id": ObjectId(user_id), "updated_at": utcnow()}
    _db().student_profiles.update_one({"user_id": ObjectId(user_id)}, {"$set": profile}, upsert=True)


def get_profile(user_id):
    return _db().student_profiles.find_one({"user_id": ObjectId(user_id)})


def update_user(user_id, fields):
    allowed = {k: v for k, v in fields.items() if k in {"full_name", "password_hash"}}
    if allowed:
        _db().users.update_one({"_id": ObjectId(user_id)}, {"$set": allowed})


def create_auth_session(user_id, token_hash, expires_at):
    return _db().auth_sessions.insert_one({
        "user_id": ObjectId(user_id),
        "token_hash": token_hash,
        "expires_at": expires_at,
        "created_at": utcnow(),
    })


def find_auth_session(token_hash):
    return _db().auth_sessions.find_one({
        "token_hash": token_hash,
        "expires_at": {"$gt": utcnow()},
    })


def revoke_auth_session(token_hash):
    _db().auth_sessions.delete_one({"token_hash": token_hash})


def save_password_reset_token(user_id, token_hash, expires_at):
    _db().users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "password_reset_token_hash": token_hash,
            "password_reset_expires_at": expires_at,
        }},
    )


def reset_password_with_token(token_hash, password_hash):
    now = utcnow()
    token_query = {
        "password_reset_token_hash": token_hash,
        "password_reset_expires_at": {"$gt": now},
    }
    user = _db().users.find_one(token_query, {"_id": 1})
    if not user:
        return False

    result = _db().users.update_one(
        {"_id": user["_id"], **token_query},
        {"$set": {"password_hash": password_hash},
         "$unset": {
             "password_reset_token_hash": "",
             "password_reset_expires_at": "",
         }},
    )
    if result.matched_count != 1:
        return False

    _db().auth_sessions.delete_many({"user_id": user["_id"]})
    return True


def save_assessment(record):
    record["user_id"] = ObjectId(record["user_id"])
    record["created_at"] = utcnow()
    return str(_db().assessments.insert_one(record).inserted_id)


def get_assessments(user_id, limit=20):
    return list(_db().assessments.find({"user_id": ObjectId(user_id)}).sort("created_at", -1).limit(limit))


def save_quiz(record):
    record["user_id"] = ObjectId(record["user_id"])
    record["created_at"] = utcnow()
    return str(_db().quiz_attempts.insert_one(record).inserted_id)


def get_quizzes(user_id, limit=20):
    return list(_db().quiz_attempts.find({"user_id": ObjectId(user_id)}).sort("created_at", -1).limit(limit))


def save_topic_progress(user_id, subject, topic, mastery_score, attempts=1):
    if mastery_score >= 90:
        status = "Strong mastery"
    elif mastery_score >= 70:
        status = "Good understanding"
    elif mastery_score >= 40:
        status = "Developing understanding"
    else:
        status = "Needs foundational teaching"
    now = utcnow()
    _db().topic_progress.update_one(
        {"user_id": ObjectId(user_id), "subject": subject, "topic": topic},
        {"$set": {"mastery_score": mastery_score, "mastery_status": status,
                  "attempts": attempts, "last_assessed": now, "updated_at": now}},
        upsert=True
    )


def get_topic_progress(user_id):
    return list(_db().topic_progress.find({"user_id": ObjectId(user_id)}).sort("updated_at", -1))


def save_learning_plan(user_id, plan):
    plan = {**plan, "user_id": ObjectId(user_id), "completion_status": {}, "created_at": utcnow()}
    return str(_db().learning_plans.insert_one(plan).inserted_id)


def get_learning_plans(user_id, limit=10):
    return list(_db().learning_plans.find({"user_id": ObjectId(user_id)}).sort("created_at", -1).limit(limit))


def save_conversation(user_id, conversation_id, topic, messages):
    now = utcnow()
    _db().tutor_conversations.update_one(
        {"conversation_id": conversation_id, "user_id": ObjectId(user_id)},
        {"$set": {"topic": topic, "messages": messages, "updated_at": now},
         "$setOnInsert": {"created_at": now}},
        upsert=True
    )


def get_conversations(user_id, limit=20):
    return list(_db().tutor_conversations.find({"user_id": ObjectId(user_id)}).sort("updated_at", -1).limit(limit))
