"""Test keyword match classifier."""

import datetime

import pandas as pd

from phiphi.pipeline_jobs import constants as pipeline_jobs_constants
from phiphi.pipeline_jobs import project_db_schemas
from phiphi.pipeline_jobs import utils as pipeline_jobs_utils
from phiphi.pipeline_jobs.classify import flow as classify_flow


def test_keyword_match_classifier(tmp_bq_project):
    """Test the keyword match classifier."""
    test_project_namespace = tmp_bq_project

    # Create dummy data to insert into BigQuery that conforms to the table schema
    deduped_general_messages_df = project_db_schemas.generalised_messages_schema.example(6)

    # Fill test data with matching and non-matching messages
    deduped_general_messages_df["phoenix_platform_message_id"] = ["a", "b", "c", "d", "e", "f"]
    deduped_general_messages_df["pi_text"] = [
        "I love apples and bananas.",
        "I love apples and oranges.",
        "I love oranges and bananas.",
        "I love oranges and apples.",
        "I love bananas and turnips.",
        "I love bananas and furthermore \n I love apples.",
    ]

    # Step 1: Add the first five messages (all except the last one) to the database
    partial_messages_df = deduped_general_messages_df.iloc[:5]

    validated_partial_messages_df = project_db_schemas.generalised_messages_schema.validate(
        partial_messages_df
    )

    pipeline_jobs_utils.write_data(
        df=validated_partial_messages_df,
        dataset=test_project_namespace,
        table=pipeline_jobs_constants.DEDUPLICATED_GENERALISED_MESSAGES_TABLE_NAME,
    )

    # Step 2: Instantiate the KeywordMatchClassifierPipeline to match the test data. Everything but
    # id "e" should match a class
    classifier = {
        "id": 1,
        "project_id": 10,
        "name": "test_classifier",
        "type": "keyword_match",
        "latest_version": {
            "version_id": 1,
            "classifier_id": 1,
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "classes": [
                {"name": "apple_banana", "description": "Things that are apples and bananas"},
                {"name": "apple_orange", "description": "Things that are apples and oranges"},
                {"name": "orange_banana", "description": "Things that are oranges and bananas"},
            ],
            "params": {
                "class_to_keyword_configs": [
                    {"class_name": "apple_banana", "musts": "apples bananas"},
                    {"class_name": "apple_orange", "musts": "apples oranges"},
                    {"class_name": "orange_banana", "musts": "oranges bananas"},
                ]
            },
        },
    }

    expected_classified_messages_df = pd.DataFrame(
        {
            "classifier_id": [1, 1, 1, 1],
            "classifier_version_id": [1, 1, 1, 1],
            "class_name": [
                "apple_banana",
                "apple_orange",
                "orange_banana",
                "apple_orange",
            ],
            "phoenix_platform_message_id": ["a", "b", "c", "d"],
            "job_run_id": [9, 9, 9, 9],
        }
    )

    # Step 3: Run the classifier for the first time
    classify_flow.classify_flow(
        classifier_dict=classifier, project_namespace=test_project_namespace, job_run_id=9
    )

    # Step 4: Check the classified messages table
    classified_messages_df = pd.read_gbq(
        f"SELECT * "
        f"FROM {test_project_namespace}.{pipeline_jobs_constants.CLASSIFIED_MESSAGES_TABLE_NAME}"
    )

    # pd.testing using check_like=True doesn't work due to dtypes, so we'll use set comparison
    set1 = set(classified_messages_df.itertuples(index=False, name=None))
    set2 = set(expected_classified_messages_df.itertuples(index=False, name=None))
    assert set1 == set2, "DataFrames contain different rows after first classification"

    # Step 5: Add the remaining message to the database (the last row)
    remaining_message_df = deduped_general_messages_df.iloc[5:]
    validated_remaining_message_df = project_db_schemas.generalised_messages_schema.validate(
        remaining_message_df
    )

    pipeline_jobs_utils.write_data(
        df=validated_remaining_message_df,
        dataset=test_project_namespace,
        table=pipeline_jobs_constants.DEDUPLICATED_GENERALISED_MESSAGES_TABLE_NAME,
    )

    # Step 6: Check classifier is incremental - i.e. running the same classifier again should not
    # duplicate the classified messages, and should classify all new messages (the last one)
    classify_flow.classify_flow(
        classifier_dict=classifier, project_namespace=test_project_namespace, job_run_id=10
    )

    # Step 7: Check the classified messages table after rerun
    post_rerun_classified_messages_df = pd.read_gbq(
        f"SELECT * "
        f"FROM {test_project_namespace}.{pipeline_jobs_constants.CLASSIFIED_MESSAGES_TABLE_NAME}"
    )

    # Update the expected DataFrame to include the last message
    new_message_df = pd.DataFrame(
        {
            "classifier_id": [1],
            "classifier_version_id": [1],
            "class_name": ["apple_banana"],
            "phoenix_platform_message_id": ["f"],
            "job_run_id": [10],
        }
    )
    expected_classified_messages_df = pd.concat(
        [expected_classified_messages_df, new_message_df], ignore_index=True
    )

    set3 = set(post_rerun_classified_messages_df.itertuples(index=False, name=None))
    set4 = set(expected_classified_messages_df.itertuples(index=False, name=None))
    assert set3 == set4, "DataFrames contain different rows after adding the last message"
