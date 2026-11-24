import re


def valid_email(value):
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value.strip()))


def password_errors(value):
    errors = []
    if len(value) < 8:
        errors.append("Use at least 8 characters")
    if not re.search(r"[A-Za-z]", value) or not re.search(r"\d", value):
        errors.append("Include at least one letter and one number")
    return errors
