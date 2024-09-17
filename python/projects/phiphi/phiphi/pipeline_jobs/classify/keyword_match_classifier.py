"""Keyword match classifier module."""
import prefect
from google.cloud import bigquery

from phiphi.api.projects.classifiers import schemas
from phiphi.pipeline_jobs import constants as pipeline_jobs_constants


@prefect.task
def classify(
    classifier: schemas.ClassifierKeywordMatchResponse, bigquery_dataset: str, job_run_id: int
) -> None:
    """Classify messages using keyword match classifier through BigQuery query."""
    client = bigquery.Client()
    classifier_id: int = classifier.id
    source_table_name = f"{bigquery_dataset}.{pipeline_jobs_constants.DEDUPLICATED_GENERALISED_MESSAGES_TABLE_NAME}"  # noqa: E501
    destination_table_name = (
        f"{bigquery_dataset}.{pipeline_jobs_constants.CLASSIFIED_MESSAGES_TABLE_NAME}"  # noqa: E501
    )

    for config in classifier.params.class_to_keyword_configs:
        class_id = config.class_id
        must_keywords = config.musts.split()

        # Construct the query conditions for each keyword.
        # BigQuery doesn't support lookarounds, so we're doing a simple LIKE.
        conditions = [f"pi_text LIKE '%{keyword}%'" for keyword in must_keywords]
        combined_conditions = " AND ".join(conditions)

        # BigQuery SQL query to classify messages and insert into the classified messages table
        query = f"""
            INSERT INTO `{destination_table_name}`
            (classifier_id, class_id, phoenix_platform_message_id, job_run_id)
            SELECT
                {classifier_id} AS classifier_id,
                {class_id} AS class_id,
                phoenix_platform_message_id,
                {job_run_id} AS job_run_id
            FROM
                `{source_table_name}`
            WHERE
                {combined_conditions}
            """

        query_job = client.query(query)
        query_job.result()
