from pymongo.errors import DuplicateKeyError
from auth.password_manager import hash_password, verify_password
from database.database_operations import create_user, find_user_by_email


def register(full_name, email, password):
    try:
        return create_user(full_name, email, hash_password(password))
    except DuplicateKeyError:
        raise ValueError("An account with this email already exists")


def authenticate(email, password):
    user = find_user_by_email(email)
    if not user or not verify_password(password, user["password_hash"]):
        return None
    if not user.get("is_active", True):
        return None
    return user
