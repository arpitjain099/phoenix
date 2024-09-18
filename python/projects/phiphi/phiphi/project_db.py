"""Project database module.

!!! IMPORTANT !!!
Metadata should only be used and an ORM should not be used for bigquery tables.
This is because bigquery does not support auto incrementing and applies constraints
using a different DDL syntax.
As such sqlalchemy.Tables should be used to define tables and developers not define primary keys or
indexes. Primary keys and indexes should not be done using sqlalchemy but rather using alembic
migrations that have `op.execute` to run the correct DDL commands. See alembic docs:
https://googleapis.dev/python/sqlalchemy-bigquery/latest/alembic.html

See docs: https://googleapis.dev/python/sqlalchemy-bigquery/latest/README.html
"""
import sqlalchemy as sa

# DO NOT USE ORM MODELS FOR BIGQUERY TABLES. See file docstring.
metadata = sa.MetaData()
