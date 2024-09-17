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
import contextlib
from typing import Generator

import sqlalchemy as sa

from phiphi import utils

# DO NOT USE ORM MODELS FOR BIGQUERY TABLES. See file docstring.
metadata = sa.MetaData()


def form_bigquery_sqlalchmey_uri(
    project_namespace: str, google_cloud_project: None | str = None
) -> str:
    """Form the bigquery sqlalchemy uri.

    Args:
        project_namespace (str): The project namespace.
        google_cloud_project (None | str, optional): The google cloud project. If None then this
            will be inferred from the google cloud auth configuration.

    Returns:
        str: The sqlalchemy uri.
    """
    if google_cloud_project is None:
        google_cloud_project = utils.get_default_bigquery_project()
    return f"bigquery://{google_cloud_project}/{project_namespace}"


@contextlib.contextmanager
def init_connection(sqlalchemy_uri: str) -> Generator[sa.Connection, None, None]:
    """Initialize a connection.

    In general Sessions are used for ORM and Connections are used for raw SQL. Since it is not
    recommended to use ORM for bigquery tables, this function is provided to get a connection.

    Args:
        sqlalchemy_uri (str): The sqlalchemy uri.

    Yields:
        Generator[Connection, None, None]: The connection.
    """
    engine = sa.create_engine(sqlalchemy_uri)
    with engine.connect() as connection:
        yield connection
