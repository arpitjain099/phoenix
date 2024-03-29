"""Test PhoenixCustomSsoSecurityManager.

Currently it is a copy of the flask_appbuilder version but with passing linting.
https://github.com/dpgaspar/Flask-AppBuilder/blob/c65e067f09e741c00322221263c8599b8e8811d5/tests/security/test_auth_remote_user.py

"""
import unittest

from flask import Flask
from flask_appbuilder import SQLA, AppBuilder  # type: ignore[import-untyped]
from flask_appbuilder.const import AUTH_REMOTE_USER  # type: ignore[import-untyped]


class AuthRemoteUserTestCase(unittest.TestCase):
    """Test PhoenixCustomSsoSecurityManager."""

    def setUp(self):
        """Set up the test."""
        # start Flask
        self.app = Flask(__name__)
        self.app.config["AUTH_TYPE"] = AUTH_REMOTE_USER

        # start Database
        self.db = SQLA(self.app)

    def tearDown(self):
        """Tear down the test."""
        # Remove test user
        user_alice = self.appbuilder.sm.find_user("alice")
        if user_alice:
            self.db.session.delete(user_alice)
            self.db.session.commit()

        # stop Flask
        self.app = None

        # stop Flask-AppBuilder
        self.appbuilder = None

        # stop Database
        self.db.session.remove()
        self.db = None

    def test_unset_remote_user_env_var(self):
        """Test unset remote user environment variable."""
        self.appbuilder = AppBuilder(self.app, self.db.session)
        sm = self.appbuilder.sm

        self.assertEqual(sm.auth_remote_user_env_var, "REMOTE_USER")

    def test_set_remote_user_env_var(self):
        """Test set remote user environment variable."""
        self.app.config["AUTH_REMOTE_USER_ENV_VAR"] = "HTTP_REMOTE_USER"
        self.appbuilder = AppBuilder(self.app, self.db.session)
        sm = self.appbuilder.sm

        self.assertEqual(sm.auth_remote_user_env_var, "HTTP_REMOTE_USER")

    def test_normal_login(self):
        """Test normal login."""
        self.appbuilder = AppBuilder(self.app, self.db.session)
        sm = self.appbuilder.sm

        # register a user
        _ = sm.add_user(
            username="alice",
            first_name="Alice",
            last_name="Doe",
            email="alice@example.com",
            role=[],
        )

        self.assertTrue(sm.auth_user_remote_user("alice"))

    def test_inactive_user_login(self):
        """Test inactive user login."""
        self.appbuilder = AppBuilder(self.app, self.db.session)
        sm = self.appbuilder.sm

        # register a user
        alice_user = sm.add_user(
            username="alice",
            first_name="Alice",
            last_name="Doe",
            email="alice@example.com",
            role=[],
        )
        alice_user.active = False
        self.assertFalse(sm.auth_user_remote_user("alice"))
