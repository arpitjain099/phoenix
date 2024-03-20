#!/bin/bash

cd /app/projects/phiphi/

# Run alembic migrations
alembic upgrade head

# Seed the database
python phiphi/seed/main.py

# Important to move back to working directory
cd -

exec $@
