"""Integration tests for the data pipeline with big query."""
import uuid

import pandas as pd
import pytest
from google.cloud import bigquery

from phiphi.pipeline_jobs import projects
from phiphi.pipeline_jobs.gathers import constants
from phiphi.pipeline_jobs.gathers import flow as gather_flow
from phiphi.tests.pipeline_jobs.gathers import example_gathers


def test_bq_pipeline_integration(session_context, reseed_tables):
    """Test pipeline integration with bigquery.

    WARNING: !!!!!!!!!!!!!!
    The patch settings fixture/monkey patching env vars does not work with Prefect flows.

    This creates a Bigquery dataset with name `test_<random_prefix>`.

    Then runs a gather flow using sample example data (no Apify calls, unless you override the
    projects settings to disable using Mock apify).

    Finally, it deletes the dataset.

    If the test fails you may need to manually clean up (delete) the dataset within Bigquery.
    """
    temp_project_namespace = str(uuid.uuid4())[:10]
    temp_project_namespace = temp_project_namespace.replace("-", "")
    test_project_namespace = f"test_{temp_project_namespace}"
    print(f"Test project namespace: {test_project_namespace}")

    dataset = projects.init_project_db.fn(test_project_namespace)
    client = bigquery.Client()
    assert client.get_dataset(dataset)

    # Check that will not fail if the dataset already exists.
    dataset = projects.init_project_db.fn(test_project_namespace)
    assert client.get_dataset(dataset)

    gather_instance = example_gathers.facebook_posts_gather_example()
    # Using patch_settings and mocking APIFY_API_KEYS does not work here
    # You need to set this in the environment
    gather_flow.gather_flow(
        gather_dict=gather_instance.dict(),
        gather_schema_name=gather_instance.__class__.__name__,
        job_run_id=1,
        project_namespace=test_project_namespace,
        batch_size=3,
    )

    messages_df = pd.read_gbq(
        f"SELECT * FROM {test_project_namespace}.{constants.GENERALISED_MESSAGES_TABLE_NAME}"
    )
    assert len(messages_df) == 8

    projects.delete_project_db.fn(test_project_namespace)
    with pytest.raises(Exception):
        client.get_dataset(dataset)
