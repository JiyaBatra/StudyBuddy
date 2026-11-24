import hashlib
import unittest
from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import patch

from bson import ObjectId

from auth import session_manager


class SessionManagerTests(unittest.TestCase):
    def test_login_stores_hashed_server_token_and_persistent_cookie(self):
        state = _SessionState()
        cookies = _FakeCookies()
        user = {"_id": ObjectId(), "full_name": "Student", "email": "student@example.com"}
        with (
            patch.object(session_manager, "st", SimpleNamespace(session_state=state)),
            patch.object(session_manager, "create_auth_session") as create_session,
            patch.dict("os.environ", {"APP_BASE_URL": "https://learnwise.example.com"}),
        ):
            session_manager.login(user, cookies)

        raw_token = cookies.values[session_manager.COOKIE_NAME]
        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
        self.assertEqual(create_session.call_args.args[:2], (str(user["_id"]), token_hash))
        self.assertEqual(cookies.options["max_age"], int(timedelta(days=30).total_seconds()))
        self.assertTrue(cookies.options["secure"])
        self.assertEqual(state["auth_token_hash"], token_hash)
        self.assertNotEqual(state["auth_token_hash"], raw_token)

    def test_init_session_restores_user_from_valid_cookie(self):
        state = _SessionState()
        user_id = ObjectId()
        user = {"_id": user_id, "full_name": "Student", "email": "student@example.com"}
        cookies = _FakeCookies({session_manager.COOKIE_NAME: "remember-token"})
        with (
            patch.object(session_manager, "st", SimpleNamespace(session_state=state)),
            patch.object(session_manager, "CookieController", return_value=cookies),
            patch.object(session_manager, "find_auth_session", return_value={"user_id": user_id}),
            patch.object(session_manager, "find_user_by_id", return_value=user),
            patch.object(session_manager, "render_background_video"),
        ):
            returned_cookies = session_manager.init_session()

        self.assertIs(returned_cookies, cookies)
        self.assertTrue(state["authenticated"])
        self.assertEqual(state["user_id"], str(user_id))
        self.assertEqual(
            state["auth_token_hash"],
            hashlib.sha256(b"remember-token").hexdigest(),
        )

    def test_init_session_removes_cookie_with_revoked_session(self):
        state = _SessionState()
        cookies = _FakeCookies({session_manager.COOKIE_NAME: "revoked-token"})
        with (
            patch.object(session_manager, "st", SimpleNamespace(session_state=state)),
            patch.object(session_manager, "CookieController", return_value=cookies),
            patch.object(session_manager, "find_auth_session", return_value=None),
            patch.object(session_manager, "render_background_video"),
        ):
            session_manager.init_session()

        self.assertNotIn(session_manager.COOKIE_NAME, cookies.values)
        self.assertFalse(state["authenticated"])

    def test_logout_revokes_persistent_session(self):
        state = _SessionState(authenticated=True, auth_token_hash="hashed-token")
        with (
            patch.object(session_manager, "st", SimpleNamespace(session_state=state)),
            patch.object(session_manager, "revoke_auth_session") as revoke_session,
        ):
            session_manager.logout()

        revoke_session.assert_called_once_with("hashed-token")
        self.assertEqual(state, {})


class _SessionState(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as exc:
            raise AttributeError(key) from exc

    def __setattr__(self, key, value):
        self[key] = value


class _FakeCookies:
    def __init__(self, values=None):
        self.values = values or {}
        self.options = {}

    def get(self, name):
        return self.values.get(name)

    def set(self, name, value, **options):
        self.values[name] = value
        self.options = options

    def remove(self, name, **options):
        self.options = options
        self.values.pop(name, None)


if __name__ == "__main__":
    unittest.main()
