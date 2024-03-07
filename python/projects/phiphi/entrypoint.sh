#!/bin/bash

cd /app/projects/phiphi/

# Run alembic migrations
alembic upgrade head

# Important to move back to working directory
cd -

exec $@
