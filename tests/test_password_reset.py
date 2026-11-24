import hashlib
import os
import re
import unittest
from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import Mock, patch
from urllib.parse import parse_qs, unquote, urlparse

from bson import ObjectId

from auth.password_reset import request_password_reset
from database import database_operations


class PasswordResetTests(unittest.TestCase):
    def test_request_sends_one_time_link_and_persists_only_token_hash(self):
        user = {
            "_id": ObjectId(),
            "email": "student@example.com",
            "full_name": "StudyBuddy Student",
        }
        response = Mock()
        with (
            patch.dict(os.environ, {
                "RESEND_API_KEY": "test-key",
                "RESEND_FROM_EMAIL": "StudyBuddy <studybuddy@example.com>",
                "APP_BASE_URL": "https://learnwise.example.com",
            }, clear=False),
            patch("auth.password_reset.find_user_by_email", return_value=user),
            patch("auth.password_reset.save_password_reset_token") as save_token,
            patch("auth.password_reset.requests.post", return_value=response) as send_email,
        ):
            request_password_reset(user["email"])

        payload = send_email.call_args.kwargs
        self.assertEqual(payload["headers"]["Authorization"], "Bearer test-key")
        self.assertEqual(payload["json"]["to"], [user["email"]])
        self.assertEqual(payload["timeout"], (3, 10))
        match = re.search(r'href="([^"]+)"', payload["json"]["html"])
        self.assertIsNotNone(match)
        reset_url = unquote(match.group(1))
        token = parse_qs(urlparse(reset_url).query)["reset"][0]
        self.assertEqual(
            save_token.call_args.args[1],
            hashlib.sha256(token.encode("utf-8")).hexdigest(),
        )
        self.assertNotEqual(save_token.call_args.args[1], token)
        response.raise_for_status.assert_called_once()

    def test_unknown_email_does_not_send_email(self):
        with (
            patch.dict(os.environ, {
                "RESEND_API_KEY": "test-key",
                "RESEND_FROM_EMAIL": "StudyBuddy <studybuddy@example.com>",
            }, clear=False),
            patch("auth.password_reset.find_user_by_email", return_value=None),
            patch("auth.password_reset.requests.post") as send_email,
        ):
            request_password_reset("unknown@example.com")

        send_email.assert_not_called()

    def test_missing_resend_configuration_fails_before_looking_up_account(self):
        with (
            patch.dict(os.environ, {
                "RESEND_API_KEY": "",
                "RESEND_FROM_EMAIL": "",
            }, clear=False),
            patch("auth.password_reset.dotenv_values", return_value={}),
            patch("auth.password_reset.find_user_by_email") as find_user,
            patch("auth.password_reset.requests.post") as send_email,
        ):
            with self.assertRaisesRegex(RuntimeError, "RESEND_API_KEY"):
                request_password_reset("student@example.com")

        find_user.assert_not_called()
        send_email.assert_not_called()

    def test_reads_updated_env_file_when_process_environment_is_stale(self):
        user = {
            "_id": ObjectId(),
            "email": "student@example.com",
            "full_name": "StudyBuddy Student",
        }
        with (
            patch.dict(os.environ, {
                "RESEND_API_KEY": "",
                "RESEND_FROM_EMAIL": "",
                "APP_BASE_URL": "",
            }, clear=False),
            patch("auth.password_reset.dotenv_values", return_value={
                "RESEND_API_KEY": "test-key",
                "RESEND_FROM_EMAIL": "StudyBuddy <studybuddy@example.com>",
                "APP_BASE_URL": "https://learnwise.example.com",
            }),
            patch("auth.password_reset.find_user_by_email", return_value=user),
            patch("auth.password_reset.save_password_reset_token"),
            patch("auth.password_reset.requests.post") as send_email,
        ):
            request_password_reset(user["email"])

        self.assertEqual(send_email.call_args.kwargs["headers"]["Authorization"], "Bearer test-key")
        self.assertIn("https://learnwise.example.com/?reset=", send_email.call_args.kwargs["json"]["text"])

    def test_password_reset_token_is_one_time_and_revokes_sessions(self):
        token_hash = "hashed-reset-token"
        database = _FakeDatabase(token_hash)
        with patch.object(database_operations, "_db", return_value=database):
            self.assertTrue(database_operations.reset_password_with_token(token_hash, "new-hash"))
            self.assertFalse(database_operations.reset_password_with_token(token_hash, "other-hash"))

        self.assertEqual(database.users.document["password_hash"], "new-hash")
        self.assertNotIn("password_reset_token_hash", database.users.document)
        self.assertEqual(database.auth_sessions.deleted_for_user, database.users.document["_id"])

    def test_expired_password_reset_token_is_rejected(self):
        token_hash = "expired-reset-token"
        database = _FakeDatabase(token_hash, expires_in=timedelta(seconds=-1))
        with patch.object(database_operations, "_db", return_value=database):
            self.assertFalse(database_operations.reset_password_with_token(token_hash, "new-hash"))

        self.assertNotIn("password_hash", database.users.document)
        self.assertIsNone(database.auth_sessions.deleted_for_user)


class _FakeCollection:
    def __init__(self, document=None):
        self.document = document
        self.deleted_for_user = None

    def find_one(self, query, _projection=None):
        if self.document is None:
            return None
        if self.document.get("password_reset_token_hash") != query.get("password_reset_token_hash"):
            return None
        expiry = self.document.get("password_reset_expires_at")
        if not expiry or expiry <= query["password_reset_expires_at"]["$gt"]:
            return None
        fields = _projection or {"_id": 1}
        return {field: self.document[field] for field in fields if field in self.document}

    def update_one(self, query, update):
        if self.find_one(query) is None:
            return SimpleNamespace(matched_count=0)
        self.document.update(update["$set"])
        for field in update["$unset"]:
            self.document.pop(field, None)
        return SimpleNamespace(matched_count=1)

    def delete_many(self, query):
        self.deleted_for_user = query["user_id"]


class _FakeDatabase:
    def __init__(self, token_hash, expires_in=timedelta(minutes=10)):
        self.users = _FakeCollection({
            "_id": ObjectId(),
            "password_reset_token_hash": token_hash,
            "password_reset_expires_at": database_operations.utcnow() + expires_in,
        })
        self.auth_sessions = _FakeCollection()


if __name__ == "__main__":
    unittest.main()
