import hashlib
import html
import os
import secrets
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlencode

import requests
from dotenv import dotenv_values

from database.database_operations import (
    find_user_by_email,
    reset_password_with_token,
    save_password_reset_token,
    utcnow,
)

RESET_TOKEN_TTL = timedelta(minutes=30)
RESEND_API_URL = "https://api.resend.com/emails"
ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


def _token_hash(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def request_password_reset(email):
    file_settings = dotenv_values(ENV_FILE)
    api_key = (os.getenv("RESEND_API_KEY") or file_settings.get("RESEND_API_KEY") or "").strip()
    from_email = (os.getenv("RESEND_FROM_EMAIL") or file_settings.get("RESEND_FROM_EMAIL") or "").strip()
    if not api_key or not from_email:
        raise RuntimeError(
            "Password reset email is not configured. Set RESEND_API_KEY and "
            "RESEND_FROM_EMAIL in .env."
        )

    user = find_user_by_email(email)
    if not user:
        return

    token = secrets.token_urlsafe(32)
    save_password_reset_token(
        str(user["_id"]),
        _token_hash(token),
        utcnow() + RESET_TOKEN_TTL,
    )

    base_url = (
        os.getenv("APP_BASE_URL")
        or file_settings.get("APP_BASE_URL")
        or "http://localhost:8501"
    ).strip().rstrip("/")
    reset_url = f"{base_url}/?{urlencode({'reset': token})}"
    name = html.escape(user.get("full_name", "there"))
    response = requests.post(
        RESEND_API_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "from": from_email,
            "to": [user["email"]],
            "subject": "Reset your StudyBuddy password",
            "html": (
                f"<p>Hi {name},</p>"
                "<p>Use the link below to choose a new password. "
                "It expires in 30 minutes and can only be used once.</p>"
                f'<p><a href="{html.escape(reset_url, quote=True)}">Reset password</a></p>'
                "<p>If you did not request this, you can ignore this email.</p>"
            ),
            "text": (
                f"Hi {user.get('full_name', 'there')},\n\n"
                f"Reset your StudyBuddy password: {reset_url}\n\n"
                "This link expires in 30 minutes and can only be used once."
            ),
        },
        timeout=(3, 10),
    )
    response.raise_for_status()


def reset_password(token, password_hash):
    return reset_password_with_token(_token_hash(token), password_hash)
