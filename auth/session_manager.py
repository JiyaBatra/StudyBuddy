import hashlib
import os
import secrets
from datetime import timedelta

import streamlit as st
from streamlit_cookies_controller import CookieController

from database.database_operations import (
    create_auth_session,
    find_auth_session,
    find_user_by_id,
    revoke_auth_session,
    utcnow,
)
from utils.layout import render_background_video

COOKIE_NAME = "learnwise_remember"
COOKIE_CONTROLLER_KEY = "learnwise_cookie_controller"
SESSION_TTL = timedelta(days=30)


def init_session():
    for key, default in {
        "authenticated": False, "user_id": None, "user": None,
        "onboarding_complete": False, "auth_token_hash": None,
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

    cookies = CookieController(key=COOKIE_CONTROLLER_KEY)
    if not st.session_state.authenticated:
        token = cookies.get(COOKIE_NAME)
        if token:
            token_hash = _token_hash(token)
            session = find_auth_session(token_hash)
            user = find_user_by_id(str(session["user_id"])) if session else None
            if user and user.get("is_active", True):
                _set_authenticated_user(user)
                st.session_state.auth_token_hash = token_hash
            else:
                cookies.remove(COOKIE_NAME, same_site="lax")

    render_background_video()
    return cookies


def login(user, cookies):
    token = secrets.token_urlsafe(32)
    token_hash = _token_hash(token)
    expires_at = utcnow() + SESSION_TTL
    create_auth_session(str(user["_id"]), token_hash, expires_at)
    cookies.set(
        COOKIE_NAME,
        token,
        max_age=int(SESSION_TTL.total_seconds()),
        secure=os.getenv("APP_BASE_URL", "").startswith("https://"),
        same_site="lax",
    )
    _set_authenticated_user(user)
    st.session_state.auth_token_hash = token_hash


def _set_authenticated_user(user):
    st.session_state.authenticated = True
    st.session_state.user_id = str(user["_id"])
    st.session_state.user = {"full_name": user["full_name"], "email": user["email"]}


def logout():
    token_hash = st.session_state.get("auth_token_hash")
    if token_hash:
        revoke_auth_session(token_hash)
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def _token_hash(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
