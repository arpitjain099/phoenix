"""Create a table with the schema from schema_path.

Usage:
    python create_gcp_tabulated_table.py <table_id>

Arguments:
    table_id (str): The table id.
    schema_path (str|None): The path read the schema from.
            default: "tabulated_messages.schema.json"
"""
import argparse

from google.cloud import bigquery

from phiphi.pipeline_jobs.tabulate import refresh_gcp_table_schema


def create_table(table_id: str, schema_path: str | None = None) -> None:
    """Create a table with the schema from schema_path.

    Args:
        table_id (str): The table id.
        schema_path (str|None): The path read the schema from.
            default: "tabulated_messages.schema.json"
    """
    if not table_id:
        raise ValueError("table_id is required.")
    if not schema_path:
        schema_path = refresh_gcp_table_schema.get_default_schema_path()

    client = bigquery.Client()

    schema = client.schema_from_json(schema_path)

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # API request
    print(f"Created table {table_id}.")


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
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    create_table(args.table_id, args.schema_path)
