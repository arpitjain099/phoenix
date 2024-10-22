"""Keyword match classifier module."""
import prefect
from google.cloud import bigquery

from phiphi.api.projects.classifiers.keyword_match import schemas
from phiphi.pipeline_jobs import constants as pipeline_jobs_constants


@prefect.task
def classify(
    classifier: schemas.KeywordMatchClassifierPipeline, bigquery_dataset: str, job_run_id: int
) -> None:
    """Classify messages using keyword match classifier through BigQuery query."""
    client = bigquery.Client()
    source_table_name = f"{bigquery_dataset}.{pipeline_jobs_constants.DEDUPLICATED_GENERALISED_MESSAGES_TABLE_NAME}"  # noqa: E501
    destination_table_name = (
        f"{bigquery_dataset}.{pipeline_jobs_constants.CLASSIFIED_MESSAGES_TABLE_NAME}"  # noqa: E501
    )

    select_statements = []
    # Loop through each config and construct a separate SELECT statement for each class
    for config in classifier.latest_version.params["class_to_keyword_configs"]:
        conditions = [f"pi_text LIKE '%{keyword}%'" for keyword in config["musts"].split()]
        combined_conditions = " AND ".join(conditions)

        select_statements.append(
            f"""
            SELECT
                {classifier.id} AS classifier_id,
                {classifier.latest_version.version_id} AS classifier_version_id,
                '{config["class_name"]}' AS class_name,
                phoenix_platform_message_id,
                {job_run_id} AS job_run_id
            FROM
                `{source_table_name}`
            WHERE
                {combined_conditions}
            """
        )

    union_query = " UNION ALL ".join(select_statements)

    query = f"""
        INSERT INTO `{destination_table_name}`
        (
            classifier_id,
            classifier_version_id,
            class_name,
            phoenix_platform_message_id,
            job_run_id
        )
        {union_query}
    """

    query_job = client.query(query)
    query_job.result()
