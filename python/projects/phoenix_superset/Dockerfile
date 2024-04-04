# Superset version must be the same as in `requirements.in`
FROM apache/superset:3.1.1

# /app/pythonpath is the directory where the pythonpath is set to
# for superset and allows use to use:
# from phoenix_superset import custom_sso_manager
# in the superset_config.py file
COPY phoenix_superset/ /app/pythonpath/phoenix_superset/

# Copy and phoenix_superset/config.py file
COPY ./config.py /app/phoenix_superset/config.py
