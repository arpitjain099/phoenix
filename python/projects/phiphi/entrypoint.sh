#!/bin/bash

cd /app/projects/phiphi/

# Run alembic migrations
alembic upgrade heads

# Important to move back to working directory
cd -

exec $@
