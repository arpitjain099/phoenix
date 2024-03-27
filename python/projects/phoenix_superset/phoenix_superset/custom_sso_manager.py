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

from flask import flash, g, redirect, request
from flask_appbuilder._compat import as_unicode
from flask_appbuilder.security.const import LOGMSG_WAR_SEC_LOGIN_FAILED
from flask_appbuilder.security.views import AuthView
from flask_appbuilder.utils.base import get_safe_redirect
from flask_appbuilder.views import expose
from flask_login import login_user
from superset.security import SupersetSecurityManager
from werkzeug.wrappers import Response as WerkzeugResponse

logger = logging.getLogger(__name__)


class AutheRemoteUserViewCustom(AuthView):
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


class PhoenixCustomSsoSecurityManager(SupersetSecurityManager):
    """Custom SSO Security Manager for Superset.

    Based on:
    https://github.com/dpgaspar/Flask-AppBuilder/blob/master/flask_appbuilder/security/manager.py#L1340-L1368
    """

    authremoteuserview = AutheRemoteUserViewCustom

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
