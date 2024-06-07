"""Deduplicate functionality for the gather pipeline job."""
import prefect
from google.cloud import bigquery

from phiphi.pipeline_jobs import constants


@prefect.task
def refresh_deduplicated_messages_tables(
    bigquery_dataset: str,
) -> None:
    """Task which takes messages table and produces a de-duplicated version."""
    client = bigquery.Client()

    source_table_name = f"{bigquery_dataset}.{constants.GENERALISED_MESSAGES_TABLE_NAME}"
    deduped_table_name = (
        f"{bigquery_dataset}.{constants.DEDUPLICATED_GENERALISED_MESSAGES_TABLE_NAME}"
    )

    dedupe_query = f"""
    CREATE OR REPLACE TABLE `{deduped_table_name}` AS
    WITH time_ordered_messages AS (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY platform, data_type, phoenix_platform_message_id
                ORDER BY platform_message_last_updated_at DESC, phoenix_processed_at DESC
            ) AS row_num
        FROM
            `{source_table_name}`
    )
    SELECT
        * EXCEPT (row_num)
    FROM
        time_ordered_messages
    WHERE
        row_num = 1
    """

    dedupe_job = client.query(dedupe_query)
    dedupe_job.result()
