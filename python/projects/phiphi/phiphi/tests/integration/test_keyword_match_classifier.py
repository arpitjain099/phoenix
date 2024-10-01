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

    validated_general_mes_df = project_db_schemas.generalised_messages_schema.validate(
        deduped_general_messages_df
    )

    pipeline_jobs_utils.write_data(
        df=validated_general_mes_df,
        dataset=test_project_namespace,
        table=pipeline_jobs_constants.DEDUPLICATED_GENERALISED_MESSAGES_TABLE_NAME,
    )

    # Instantiate the ClassifierKeywordMatchResponse to match the test data. Everything but id "e"
    # should match a class
    classifier = {
        "id": 1,
        "version_id": 1,
        "project_id": 10,
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "version_created_at": datetime.datetime.now(),
        "version_updated_at": datetime.datetime.now(),
        "archived_at": None,
        "classifier_id": 1,
        "type": "keyword_match",
        "name": "test_classifier",
        "classes_dict": {
            "apple_banana": "Things that are apples and bananas",
            "apple_orange": "Things that are apples and oranges",
            "orange_banana": "Things that are oranges and bananas",
        },
        "params": {
            "class_to_keyword_configs": [
                {"class_name": "apple_banana", "musts": "apples bananas"},
                {"class_name": "apple_orange", "musts": "apples oranges"},
                {"class_name": "orange_banana", "musts": "oranges bananas"},
            ]
        },
    }

    expected_classified_messages_df = pd.DataFrame(
        {
            "classifier_id": [1, 1, 1, 1, 1],
            "classifier_version_id": [1, 1, 1, 1, 1],
            "class_name": [
                "apple_banana",
                "apple_orange",
                "orange_banana",
                "apple_orange",
                "apple_banana",
            ],
            "phoenix_platform_message_id": ["a", "b", "c", "d", "f"],
            "job_run_id": [9, 9, 9, 9, 9],
        }
    )

    # Run the classifier
    classify_flow.classify_flow(
        classifier_dict=classifier, project_namespace=test_project_namespace, job_run_id=9
    )

    # Check the classified messages table
    classified_messages_df = pd.read_gbq(
        f"SELECT * "
        f"FROM {test_project_namespace}.{pipeline_jobs_constants.CLASSIFIED_MESSAGES_TABLE_NAME}"
    )

    # pd.testing using check_like=True doesn't work due to dtypes, so we'll use set comparison
    set1 = set(classified_messages_df.itertuples(index=False, name=None))
    set2 = set(expected_classified_messages_df.itertuples(index=False, name=None))
    # Compare sets
    assert set1 == set2, "DataFrames contain different rows"
