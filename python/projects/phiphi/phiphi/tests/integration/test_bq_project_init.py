"""Test the project init function."""
import pytest
from google.cloud import bigquery

from phiphi.pipeline_jobs import constants, projects


def test_bq_project_init(temp_project_namespace):
    """Test project init function with a real Bigquery project.

    If the test fails you may need to manually clean up (delete) the dataset within Bigquery.
    """
    projects.init_project_db.fn(temp_project_namespace, with_dummy_rows=2)

    client = bigquery.Client()
    assert client.get_dataset(temp_project_namespace)
    # Check that the dummy tabulated messages has been created
    assert client.get_table(f"{temp_project_namespace}.{constants.TABULATED_MESSAGES_TABLE_NAME}")

    # Check that will not fail if the dataset already exists.
    dataset = projects.init_project_db.fn(temp_project_namespace)
    assert client.get_dataset(dataset)

    projects.delete_project_db.fn(temp_project_namespace)
    with pytest.raises(Exception):
        client.get_dataset(dataset)
