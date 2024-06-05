"""Integration tests for the data pipeline with big query."""
import uuid

import pytest
from google.cloud import bigquery

from phiphi.pipeline_jobs import projects
from phiphi.pipeline_jobs.gathers import flow as gather_flow
from phiphi.tests.pipeline_jobs.gathers import example_gathers


# !!!!!!!!!!!!!!
# Patch settings does not work with flows.
def test_bq_pipeline_integration(session_context, reseed_tables):
    """Test pipeline integration with bigquery.

    This creates a dataset with prefect `test_<random_prefix>`.

    If the test fails you may need to manually clean up the dataset.
    """
    temp_prefix = str(uuid.uuid4())[:10]
    temp_prefix = temp_prefix.replace("-", "")
    test_prefix = f"test_{temp_prefix}"
    dataset = projects.init_project_db.fn(project_id=1, namespace_prefix=test_prefix)
    client = bigquery.Client()
    assert client.get_dataset(dataset)

    # Check that will not fail if the dataset already exists.
    dataset = projects.init_project_db.fn(project_id=1, namespace_prefix=test_prefix)
    assert client.get_dataset(dataset)

    # Using patch_settings and mocking APIFY_API_KEYS does not work here
    # You need to set this in the environment
    gather_flow.gather_flow(
        gather=example_gathers.facebook_posts_gather_example(),
        job_run_id=1,
        batch_size=3,
    )

    projects.delete_project_db.fn(project_id=1, namespace_prefix=test_prefix)
    with pytest.raises(Exception):
        client.get_dataset(dataset)
