# Superset version must be the same as in `requirements.in`
FROM apache/superset:3.1.1

# /app/pythonpath is the directory where the pythonpath is set to
# for superset and allows use to use:
# from phoenix_superset import custom_sso_manager
# in the superset_config.py file
COPY phoenix_superset/ /app/pythonpath/phoenix_superset/

# Copy and set the superset_config.py file
COPY superset_config.py /app/superset_config.py
ENV SUPERSET_CONFIG_PATH=/app/superset_config.py
