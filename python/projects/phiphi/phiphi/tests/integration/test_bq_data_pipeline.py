"""Integration tests for the data pipeline with big query."""
import uuid

import pytest
from google.cloud import bigquery

from phiphi.pipeline_jobs import projects


def test_bq_pipeline_integration(session_context, reseed_tables):
    """Test pipeline integration with bigquery.

    This creates a dataset with prefect `test_<random_prefix>`.

    If the test fails you may need to manually clean up the dataset.
    """
    maxval = 10
    temp_prefix = str(uuid.uuid4())[:maxval]
    temp_prefix = temp_prefix.replace("-", "")
    test_prefix = f"test_{temp_prefix}"
    dataset = projects.init_project_db.fn(project_id=1, namespace_prefix=test_prefix)
    client = bigquery.Client()
    assert client.get_dataset(dataset)

    # Check that will not fail if the dataset already exists.
    dataset = projects.init_project_db.fn(project_id=1, namespace_prefix=test_prefix)
    assert client.get_dataset(dataset)

    projects.delete_project_db.fn(project_id=1, namespace_prefix=test_prefix)
    with pytest.raises(Exception):
        client.get_dataset(dataset)
