"""Integration tests for the data pipeline with big query."""
import uuid

import pandas as pd
import pytest
from google.cloud import bigquery

from phiphi.pipeline_jobs import constants, projects
from phiphi.pipeline_jobs.gathers import flow as gather_flow
from phiphi.pipeline_jobs.tabulate import flow as tabulate_flow
from phiphi.tests.pipeline_jobs.gathers import example_gathers


def test_bq_pipeline_integration():
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

    dataset = projects.init_project_db.fn(test_project_namespace, with_dummy_rows=2)
    client = bigquery.Client()
    assert client.get_dataset(dataset)
    # Check that the dummy tabulated messages has been created
    assert client.get_table(f"{dataset}.{constants.TABULATED_MESSAGES_TABLE_NAME}")

    # Check that will not fail if the dataset already exists.
    dataset = projects.init_project_db.fn(test_project_namespace)
    assert client.get_dataset(dataset)

    batch_size = 20
    # Using patch_settings and mocking APIFY_API_KEYS does not work here
    # You need to set this in the environment
    gather_flow.gather_flow(
        gather_dict=example_gathers.facebook_posts_gather_example().dict(),
        gather_child_type=example_gathers.facebook_posts_gather_example().child_type,
        job_run_id=1,
        project_namespace=test_project_namespace,
        batch_size=batch_size,
    )

    messages_df = pd.read_gbq(
        f"SELECT * FROM {test_project_namespace}.{constants.GENERALISED_MESSAGES_TABLE_NAME}"
    )
    assert len(messages_df) == 8

    gather_flow.gather_flow(
        gather_dict=example_gathers.facebook_posts_gather_example().dict(),
        gather_child_type=example_gathers.facebook_posts_gather_example().child_type,
        job_run_id=2,
        project_namespace=test_project_namespace,
        batch_size=batch_size,
    )

    messages_df = pd.read_gbq(
        f"SELECT * FROM {test_project_namespace}.{constants.GENERALISED_MESSAGES_TABLE_NAME}"
    )
    assert len(messages_df) == 16
    deduped_messages_df = pd.read_gbq(
        f"""
        SELECT *
        FROM {test_project_namespace}.{constants.DEDUPLICATED_GENERALISED_MESSAGES_TABLE_NAME}
        """
    )
    assert len(deduped_messages_df) == 8

    gather_flow.gather_flow(
        gather_dict=example_gathers.facebook_comments_gather_example().dict(),
        gather_child_type=example_gathers.facebook_comments_gather_example().child_type,
        job_run_id=3,
        project_namespace=test_project_namespace,
        batch_size=batch_size,
    )

    batches_df = pd.read_gbq(
        f"SELECT * FROM {test_project_namespace}.{constants.GATHER_BATCHES_TABLE_NAME}"
    )
    assert len(batches_df) == 3

    messages_df = pd.read_gbq(
        f"SELECT * FROM {test_project_namespace}.{constants.GENERALISED_MESSAGES_TABLE_NAME}"
    )
    assert len(messages_df) == 25

    tabulate_flow.tabulate_flow(job_run_id=4, project_namespace=test_project_namespace)

    deduped_messages_df = pd.read_gbq(
        f"""
        SELECT *
        FROM {test_project_namespace}.{constants.DEDUPLICATED_GENERALISED_MESSAGES_TABLE_NAME}
        """
    )
    assert len(deduped_messages_df) == 17

    tabulated_messages_df = pd.read_gbq(
        f"""
        SELECT *
        FROM {test_project_namespace}.{constants.TABULATED_MESSAGES_TABLE_NAME}
        """
    )
    assert len(tabulated_messages_df) == 14

    # Delete just the comments
    gather_id_of_comments = example_gathers.facebook_comments_gather_example().id
    gather_flow.delete_flow(
        gather_id=gather_id_of_comments,
        project_namespace=test_project_namespace,
    )

    # Checking that the comments are deleted from the batches
    batches_df = pd.read_gbq(
        f"SELECT * FROM {test_project_namespace}.{constants.GATHER_BATCHES_TABLE_NAME}"
    )
    assert len(batches_df) == 2
    assert gather_id_of_comments not in batches_df["gather_id"].unique()

    # Now the comments should be out of the generalised message table
    messages_df = pd.read_gbq(
        f"SELECT * FROM {test_project_namespace}.{constants.GENERALISED_MESSAGES_TABLE_NAME}"
    )
    assert len(messages_df) == 16
    assert gather_id_of_comments not in messages_df["gather_id"].unique()

    # and the deduplication should be the same as without the comments.
    deduped_messages_df = pd.read_gbq(
        f"""
        SELECT *
        FROM {test_project_namespace}.{constants.DEDUPLICATED_GENERALISED_MESSAGES_TABLE_NAME}
        """
    )
    assert len(deduped_messages_df) == 8
    assert gather_id_of_comments not in deduped_messages_df["gather_id"].unique()

    # Tabulate without the comments
    tabulate_flow.tabulate_flow(job_run_id=4, project_namespace=test_project_namespace)

    tabulated_messages_df = pd.read_gbq(
        f"""
        SELECT *
        FROM {test_project_namespace}.{constants.TABULATED_MESSAGES_TABLE_NAME}
        """
    )
    assert len(tabulated_messages_df) == 8

    # Use this to break before deleting the dataset to manually inspect the data
    # assert False

    projects.delete_project_db.fn(test_project_namespace)
    with pytest.raises(Exception):
        client.get_dataset(dataset)
