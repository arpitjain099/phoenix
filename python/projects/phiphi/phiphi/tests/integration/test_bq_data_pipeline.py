"""Integration tests for the data pipeline with big query."""
import uuid
from unittest.mock import patch

import pandas as pd
import pytest
from google.cloud import bigquery

from phiphi.pipeline_jobs import constants, projects
from phiphi.pipeline_jobs import utils as pipeline_jobs_utils
from phiphi.pipeline_jobs.composite_flows import delete_gather_tabulate_flow
from phiphi.pipeline_jobs.gathers import flow as gather_flow
from phiphi.pipeline_jobs.gathers import normalisers
from phiphi.pipeline_jobs.tabulate import flow as tabulate_flow
from phiphi.tests.pipeline_jobs.gathers import example_gathers


def test_bq_pipeline_integration():
    """Test pipeline integration with bigquery.

    WARNING: !!!!!!!!!!!!!!
    The patch settings fixture/monkey patching env vars does not work with Prefect flows.

    Instructions on running this test using venv (not using docker):
     - In `phiphi/config.py`:
        - Set `USE_MOCK_APIFY: bool = True`
        - Add `None` default to `SQLALCHEMY_DATABASE_URI: ... | None = None`
        - `USE_MOCK_BQ` must be false this requires a change in
          python/projects/phiphi/docker_env.dev if using `make test_integration`.
     - Login to Prefect cloud via CLI using API key from `Phoenix Dev` workspace
     - Delete everything in `tests/confest.py` and the line `engine = create_engine(...`
        in `phiphi/platform_db.py`

    This test creates a Bigquery dataset with name `test_<random_prefix>`.

    Then runs a gather flow using sample example data (no Apify calls, unless you override the
    projects settings to disable using Mock apify).

    It then checks a number of other flows and pipeline processes.

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

    # Check that if the first gather is run with no data, the table is not created This is
    # important as if we try to produce generalised_messages without any data, it will fail. We
    # could have the Apify scrape insert a gather batch that is empty but then this creates the
    # wrong schema for the generalised_messages table.
    with patch("phiphi.pipeline_jobs.gathers.utils.load_sample_raw_data", return_value=[]):
        gather_flow.gather_flow(
            gather_dict=example_gathers.facebook_posts_gather_example().dict(),
            gather_child_type=example_gathers.facebook_posts_gather_example().child_type,
            job_run_id=1,
            project_namespace=test_project_namespace,
            batch_size=batch_size,
        )

    messages_exists = pd.read_gbq(
        f"""
        SELECT COUNT(1) AS table_exists
        FROM `{test_project_namespace}.INFORMATION_SCHEMA.TABLES`
        WHERE table_name = '{constants.GENERALISED_MESSAGES_TABLE_NAME}'
        """
    )
    assert messages_exists["table_exists"][0] == 0

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
    deduped_messages_df = pd.read_gbq(
        f"""
        SELECT *
        FROM {test_project_namespace}.{constants.DEDUPLICATED_GENERALISED_MESSAGES_TABLE_NAME}
        """
    )
    assert len(deduped_messages_df) == 17

    tabulate_flow.tabulate_flow(
        job_run_id=4, project_namespace=test_project_namespace, class_id_name_map={}
    )

    tabulated_messages_df = pd.read_gbq(
        f"""
        SELECT *
        FROM {test_project_namespace}.{constants.TABULATED_MESSAGES_TABLE_NAME}
        """
    )
    assert len(tabulated_messages_df) == 14
    # Test that "class"/"comment_class" columns exists in the tabulated messages and has NaN values
    assert tabulated_messages_df["class"].isna().all()
    assert tabulated_messages_df["comment_class"].isna().all()

    # Manually create and add some classified_messages
    # Grab rows just to make a dataframe
    classified_messages_df = deduped_messages_df.iloc[:7][["phoenix_platform_message_id"]].copy()
    # Explicitly set the message IDs - this is brittle, but better than doing anything smart.
    classified_messages_df["phoenix_platform_message_id"] = [
        normalisers.anonymize("818337297005563"),  # post with no comments one class
        normalisers.anonymize("823689576453736"),  # post with 3 comments one class
        # post with 4 comments two classes
        normalisers.anonymize("823003113189049"),
        normalisers.anonymize("823003113189049"),
        # comment one class
        normalisers.anonymize("Y29tbWVudDo4MjMwMDMxMTMxODkwNDlfMTM1Njc3Njg4NDk5NzU1Mg=="),
        # comment two classes
        normalisers.anonymize("Y29tbWVudDo4MjM2ODk1NzY0NTM3MzZfMTUyMDM5OTc0ODU5MzY2NA=="),
        normalisers.anonymize("Y29tbWVudDo4MjM2ODk1NzY0NTM3MzZfMTUyMDM5OTc0ODU5MzY2NA=="),
    ]
    classified_messages_df["classifier_id"] = 1
    classified_messages_df["class_id"] = [0, -1, 0, 1, 1, 0, 1]
    classified_messages_df["job_run_id"] = 5
    pipeline_jobs_utils.write_data(
        df=classified_messages_df,
        dataset=test_project_namespace,
        table=constants.CLASSIFIED_MESSAGES_TABLE_NAME,
    )

    class_id_name_map = {0: "economy", 1: "politics"}

    # Re-tabulate, now with the classified messages, and class_id_name_map
    tabulate_flow.tabulate_flow(
        job_run_id=4, project_namespace=test_project_namespace, class_id_name_map=class_id_name_map
    )

    tabulated_messages_df = pd.read_gbq(
        f"""
        SELECT *
        FROM {test_project_namespace}.{constants.TABULATED_MESSAGES_TABLE_NAME}
        """
    )
    # This is a bit complicated, so always best to look at the actual tables in BQ if in any doubt.
    # In classified messages we did the following:
    # - Add a single class to a post which doesn't have any comments -> no change in count
    # - Add two classes to a post, BUT, that post has 4 comments, so it creates 2 * num_comments,
    # i.e. 4 _new_ rows in tabulated_messages table due to cross-product posts x comments.
    # - Add a single class to a comment -> no change in count
    # - Added a single class (without a matching class name) to a post with comments -> no change
    # in total count
    # - Added two classes to a comment -> +1 to the total count
    assert len(tabulated_messages_df) == 19  # Previous count was 14
    assert tabulated_messages_df["class"].isna().sum() == 5
    for class_name in class_id_name_map.values():
        assert class_name in tabulated_messages_df["class"].unique()
    assert "missing_class_name" in tabulated_messages_df["class"].unique()
    assert tabulated_messages_df["comment_class"].isna().sum() == 15
    for class_name in class_id_name_map.values():
        assert class_name in tabulated_messages_df["comment_class"].unique()

    # Delete just the comments
    gather_id_of_comments = example_gathers.facebook_comments_gather_example().id
    delete_gather_tabulate_flow.delete_gather_tabulate_flow(
        project_id=1,
        job_source_id=gather_id_of_comments,
        job_run_id=5,
        project_namespace=test_project_namespace,
        class_id_name_map=class_id_name_map,
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

    tabulated_messages_df = pd.read_gbq(
        f"""
        SELECT *
        FROM {test_project_namespace}.{constants.TABULATED_MESSAGES_TABLE_NAME}
        """
    )
    assert len(tabulated_messages_df) == 9

    # Use this to break before deleting the dataset to manually inspect the data
    # assert False

    projects.delete_project_db.fn(test_project_namespace)
    with pytest.raises(Exception):
        client.get_dataset(dataset)
