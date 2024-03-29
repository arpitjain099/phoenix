"""Custom SSO Manager for Superset.

This module contains a custom SSO manager for Superset that allows for
authentication via a header in the request. This is useful for integrating Superset with an
existing authentication system such as the oauth2-proxy layer we use in Phoenix.

To use this custom SSO manager, set the following configuration in your
Superset configuration file:

```python
from custom_sso_manager import PhoenixCustomSsoSecurityManager

AUTH_TYPE = AUTH_REMOTE_USER
AUTH_REMOTE_USER_ENV_VAR = "x-auth-request-email"
# Will allow user self registration, allowing to create Flask users from Authorized User
AUTH_USER_REGISTRATION = True
# The default user self registration role
AUTH_USER_REGISTRATION_ROLE = "Admin"

CUSTOM_SECURITY_MANAGER = PhoenixCustomSsoSecurityManager
```

This will override the default Superset security manager with the custom SSO
manager defined in this module.

"""
import logging
from typing import Union

from flask import g, redirect, request
from flask_appbuilder.const import (  # type: ignore[import-untyped]
    LOGMSG_WAR_SEC_LOGIN_FAILED,
)
from flask_appbuilder.security.sqla.models import User  # type: ignore[import-untyped]
from flask_appbuilder.security.views import AuthView  # type: ignore[import-untyped]
from flask_appbuilder.utils.base import get_safe_redirect  # type: ignore[import-untyped]
from flask_appbuilder.views import expose  # type: ignore[import-untyped]
from flask_login import login_user  # type: ignore[import-untyped]
from superset.security import SupersetSecurityManager  # type: ignore[import-untyped]
from werkzeug.wrappers import Response as WerkzeugResponse

logger = logging.getLogger(__name__)


class AutheRemoteUserViewCustom(AuthView):  # type: ignore[no-any-unimported]
    """Custom view for remote user authentication.

    Based on taken from:
    https://github.com/dpgaspar/Flask-AppBuilder/blob/master/flask_appbuilder/security/views.py#L729-L747
    """

    login_template = ""

    @expose("/login/")
    def login(self) -> WerkzeugResponse:
        """Login view for remote user authentication.

        Currently the same as parent.
        """
        username = request.environ.get(self.appbuilder.sm.auth_remote_user_env_var)
        if g.user is not None and g.user.is_authenticated:
            next_url = request.args.get("next", "")
            return redirect(get_safe_redirect(next_url))
        if username:
            user = self.appbuilder.sm.auth_user_remote_user(username)
            if user is None:
                flash(as_unicode(self.invalid_login_message), "warning")
            else:
                login_user(user)
        else:
            flash(as_unicode(self.invalid_login_message), "warning")
        next_url = request.args.get("next", "")
        return redirect(get_safe_redirect(next_url))


class PhoenixCustomSsoSecurityManager(SupersetSecurityManager):  # type: ignore[no-any-unimported]
    """Custom SSO Security Manager for Superset.

    Based on:
    https://github.com/dpgaspar/Flask-AppBuilder/blob/master/flask_appbuilder/security/manager.py#L1340-L1368

    The auth_remote_user_env_var has been added as the flask_appbuilder version that superset is
    currently using does not have this functionality.
    """

    authremoteuserview = AutheRemoteUserViewCustom

    def __init__(self, appbuilder) -> None:  # type: ignore[no-untyped-def]
        """Create a custom SSO security manager.

        Taken from:
        https://github.com/dpgaspar/Flask-AppBuilder/blob/master/flask_appbuilder/security/manager.py#L261-L262
        """
        super().__init__(appbuilder)
        app = self.appbuilder.get_app
        app.config.setdefault("AUTH_REMOTE_USER_ENV_VAR", "REMOTE_USER")

    @property
    def auth_remote_user_env_var(self) -> str:
        """Get the remote user environment variable.

        Taken from:
        https://github.com/dpgaspar/Flask-AppBuilder/blob/master/flask_appbuilder/security/manager.py#L426-L428
        """
        return str(self.appbuilder.get_app.config["AUTH_REMOTE_USER_ENV_VAR"])

    def auth_user_remote_user(self, username):
        """REMOTE_USER user Authentication.

        Currently the same as parent.
        """
        user = self.find_user(username=username)

        # User does not exist, create one if auto user registration.
        if user is None and self.auth_user_registration:
            user = self.add_user(
                # All we have is REMOTE_USER, so we set
                # the other fields to blank.
                username=username,
                first_name=username,
                last_name="-",
                email=username + "@email.notfound",
                role=self.find_role(self.auth_user_registration_role),
            )

        # If user does not exist on the DB and not auto user registration,
        # or user is inactive, go away.
        elif user is None or (not user.is_active):
            logger.info(LOGMSG_WAR_SEC_LOGIN_FAILED, username)
            return None

        self.update_user_auth_stat(user)
        return user
