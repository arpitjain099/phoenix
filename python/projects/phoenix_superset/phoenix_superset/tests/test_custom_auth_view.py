"""Test AutheRemoteUserViewCustom."""
import unittest

import pytest
from flask import Flask
from flask_appbuilder import SQLA, AppBuilder  # type: ignore[import-untyped]
from flask_appbuilder.const import AUTH_REMOTE_USER  # type: ignore[import-untyped]

from phoenix_superset import custom_sso_manager


class AuthRemoteUserTestCase(unittest.TestCase):
    """Test AuthRemoteUser."""

    def setUp(self):
        """Setup."""
        # start Flask
        self.app = Flask(__name__)
        self.app.config["AUTH_TYPE"] = AUTH_REMOTE_USER
        # Debug mode so that exceptions are raised instead of returning 500 responses
        # to allow for easier debugging of tests
        self.app.config["DEBUG"] = True
        self.app.config["SECRET_KEY"] = "thisismys"

        # start Database
        self.db = SQLA(self.app)

        self.client = self.app.test_client()

    def tearDown(self):
        """Tear down."""
        # Remove test user
        user_alice = self.appbuilder.sm.find_user("alice")
        if user_alice:
            self.db.session.delete(user_alice)
            self.db.session.commit()

        # stop Flask
        delattr(self, "app")

        # stop Flask-AppBuilder
        delattr(self, "appbuilder")

        # stop Database
        self.db.session.remove()
        delattr(self, "db")

    def create_appbuilder(self):
        """Create appbuilder."""
        return AppBuilder(
            self.app,
            self.db.session,
            security_manager_class=custom_sso_manager.PhoenixCustomSSOSecurityManager,
        )

    def test_login_error_with_debug(self):
        """Test login error is correct."""
        self.appbuilder = self.create_appbuilder()
        # Simulate logging in
        with self.client as c:
            with pytest.raises(Exception) as e:
                c.get("/login/")
                self.assertIn(
                    "The REMOTE_USER header is not set and no login URL",
                    str(e.value),
                )

    def test_login_error(self):
        """Test login error is correct."""
        self.app.config["DEBUG"] = False
        self.appbuilder = self.create_appbuilder()
        # Simulate logging in
        with self.client as c:
            response = c.get("/login/")
            self.assertEqual(response.status_code, 500)

    def test_login_authenticated_user(self):
        """Test login authenticated user."""
        self.appbuilder = self.create_appbuilder()
        self.client = self.app.test_client()
        sm = self.appbuilder.sm
        # register a user
        alice_user = sm.add_user(
            username="alice",
            first_name="Alice",
            last_name="Doe",
            email="alice@example.com",
            role=[],
        )
        response = self.client.get("/login/", environ_base={"REMOTE_USER": alice_user.email})
        assert response.status_code == 302  # Expecting a redirect
        # This should go back to home page
        assert response.headers["Location"] == "/"

    def test_login_not_found(self):
        """Test login authenticated user."""
        login_redirect_url = "/some_other_url"
        self.app.config["LOGIN_REDIRECT_URL"] = login_redirect_url
        self.appbuilder = self.create_appbuilder()
        sm = self.appbuilder.sm
        # register a user
        _ = sm.add_user(
            username="alice",
            first_name="Alice",
            last_name="Doe",
            email="alice@example.com",
            role=[],
        )
        response = self.client.get("/login/", environ_base={"REMOTE_USER": "NOT_FOUND"})
        assert response.status_code == 302
        assert response.headers["Location"] == login_redirect_url

    def test_login_session(self):
        """Test login authenticated user.

        Ie. if the user has a session already.
        """
        self.appbuilder = self.create_appbuilder()
        self.client = self.app.test_client()
        sm = self.appbuilder.sm
        # register a user
        alice_user = sm.add_user(
            username="alice",
            first_name="Alice",
            last_name="Doe",
            email="alice@example.com",
            role=[],
        )
        with self.client as c:
            c.get("/login/", environ_base={"REMOTE_USER": alice_user.email})
            with c.session_transaction() as sess:
                sess["_user_id"] = alice_user.id
            response = self.client.get("/login/", environ_base={"REMOTE_USER": "NOT_FOUND"})
            assert response.status_code == 302
            assert response.headers["Location"] == "/"
