"""Phoenix superset config."""
import os

from flask_appbuilder.security.manager import AUTH_REMOTE_USER  # type: ignore[import-untyped]
from phoenix_superset import custom_sso_manager

AUTH_TYPE = AUTH_REMOTE_USER

# Default of x-auth-request-email is what oauth2-proxy set up uses
AUTH_REMOTE_USER_ENV_VAR = os.getenv("AUTH_REMOTE_USER_ENV_VAR", "x-auth-request-email")

# This is needed to test the system without the authentication layer
LOGIN_REDIRECT_URL = os.getenv("LOGIN_REDIRECT_URL")

CUSTOM_SECURITY_MANAGER = custom_sso_manager.PhoenixCustomSSOSecurityManager
