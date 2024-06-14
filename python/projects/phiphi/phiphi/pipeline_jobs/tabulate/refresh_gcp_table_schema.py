"""Refresh the schema for the tabulated table.

It is recommended to run this script on a table that was created with the integration:
python/projects/phiphi/phiphi/tests/integration/test_bq_data_pipeline.py

You will need to have the test not delete the dataset at the end of the test to use this script.
See the test for how to do this.

Usage:
    python refresh_gcp_table_schema.py <table_id> <schema_path>
"""
import argparse

from google.cloud import bigquery


def refresh_tabulate_schema(table_id: str, schema_path: str) -> None:
    """Refresh the schema for the tabulated table.

    Args:
        table_id (str): The table id.
        schema_path (str): The path to write the schema to.
    """
    client = bigquery.Client()
    table = client.get_table(table_id)  # Make an API request.

    # Write a schema file to schema_path with the schema_to_json method.
    client.schema_to_json(table.schema, schema_path)

    # View table properties
    print(f"Got table '{table.project}.{table.dataset_id}.{table.table_id}'.")
    print(f"Persisted schema to {schema_path}.")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Refresh the schema for the tabulated table.")
    parser.add_argument("table_id", type=str, help="The table id.")
    parser.add_argument("schema_path", type=str, help="The path to write the schema to.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    refresh_tabulate_schema(args.table_id, args.schema_path)
