"""Utils for classified_messages BigQuery table schema."""
import pathlib


def get_path() -> str:
    """Get the schema path."""
    module_dir = pathlib.Path(__file__).resolve().parent
    return str(module_dir / "classified_messages.schema.json")
