# Superset version must be the same as in `requirements.in`
FROM apache/superset:4.0.2

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

# Install the driver requirements.
# Using an .in file rather than a .txt file as
# this is what is documented in the docker image:
# https://hub.docker.com/r/apache/superset
COPY ./docker.requirements.in /app/phoenix_superset/docker.requirements.in
USER root

RUN pip install --no-cache-dir -r /app/phoenix_superset/docker.requirements.in

USER superset

## Assets
# Copy the assets to the /app/assets directory
COPY ./assets/images/* /app/superset/static/assets/images/
