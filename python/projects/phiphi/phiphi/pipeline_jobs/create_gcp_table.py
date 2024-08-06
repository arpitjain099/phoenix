"""Create a GCP BigQuery table from schema.

Usage:
    python create_gcp_table.py <table_id> --schema_path <schema_path>

Arguments:
    table_id (str): The table id.
    schema_path (str): The path read the schema from.
"""
import argparse
from typing import Any

from google.cloud import bigquery, exceptions


def create_table(
    table_id: str,
    schema_path: str,
    with_dummy_rows: int = 0,
    exists_ok: bool = False,
) -> None:
    """Create a table with the schema from schema_path.

    Args:
        table_id (str): The table id.
        schema_path (str): The path to the schema file.
        with_dummy_rows (int): The number of dummy rows to insert into the table.
            default: 0
        exists_ok (bool): If True, do not raise an error if the table already exists.
    """
    if not table_id:
        raise ValueError("table_id is required.")
    if not schema_path:
        raise ValueError("schema_path is required.")

    client = bigquery.Client()

    schema = client.schema_from_json(schema_path)

    table = bigquery.Table(table_id, schema=schema)
    try:
        table = client.create_table(table, exists_ok=exists_ok)  # API request
        print(f"Created table {table_id}.")
    except exceptions.Conflict:
        print(f"Table {table_id} already exists.")
        print("Will not insert dummy rows.")
        return None

    if with_dummy_rows:
        print(f"Inserting {with_dummy_rows} dummy rows into {table_id}.")
        rows = [
            {field.name: get_default_value(field.field_type) for field in table.schema}
            for _ in range(with_dummy_rows)
        ]
        client.insert_rows(table, rows)
    print("Completed.")


def get_default_value(field_type: str) -> Any:
    """Get the default value for a BigQuery field type.

    Args:
        field_type (str): The BigQuery field type.

    Returns:
        any: The default value for the field type.
    """
    default_values = {
        "STRING": "dummy_string",
        "BYTES": b"dummy_bytes",
        "INTEGER": 0,
        "INT64": 0,
        "FLOAT": 0.0,
        "FLOAT64": 0.0,
        "NUMERIC": 0.0,
        "BIGNUMERIC": 0.0,
        "BOOLEAN": False,
        "BOOL": False,
        "TIMESTAMP": "1970-01-01 00:00:00 UTC",
        "DATE": "1970-01-01",
        "TIME": "00:00:00",
        "DATETIME": "1970-01-01T00:00:00",
        "GEOGRAPHY": "POINT(0 0)",
        "RECORD": {},
    }

    return default_values.get(field_type, None)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Create a table with the schema from schema_path."
    )
    parser.add_argument("table_id", type=str, help="The table id.")
    parser.add_argument(
        "--schema_path",
        type=str,
        help="The path read the schema from.",
    )
    parser.add_argument(
        "--with_dummy_rows",
        type=int,
        help="The number of dummy rows to insert into the table.",
        default=0,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    create_table(args.table_id, args.schema_path, args.with_dummy_rows)
