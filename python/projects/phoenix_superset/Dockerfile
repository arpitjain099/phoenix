# Superset version must be the same as in `requirements.in`
FROM apache/superset:3.1.1

# We are not using the default /app/pythonpath directory
# as in superset helm everything is overwritten there.
# Using /app/phoenix_superset/ as a pythonpath.
# Usage:
# `from phoenix_superset import custom_sso_manager`
# `CUSTOM_SSO_MANAGER = custom_sso_manager.PhoenixCustomSSOSecurityManager`
# in the config.py file or config override.
COPY ./phoenix_superset/ /app/phoenix_superset/phoenix_superset/
ENV PYTHONPATH=/app/phoenix_superset/:$PYTHONPATH

# Copy and phoenix_superset/config.py file
COPY ./config.py /app/phoenix_superset/config.py
