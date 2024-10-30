"""Module to check quality of the tabulated dashboard dataset."""
import prefect
from google.cloud import bigquery

from phiphi.pipeline_jobs import constants


@prefect.task
def find_post_author_gaps(bigquery_dataset: str) -> None:
    """Runs a SQL query to find months where authors don't have post data.

    Creates a table with the columns post_author_id, post_author_name_pi, post_author_link_pi,
    post_year, post_month for authors who have no posts in a given month, but posts in different
    months.

    Parameters
    bigquery_dataset : str. The BigQuery dataset to use.
    """
    client = bigquery.Client()
    tabulate_table_name = f"{bigquery_dataset}.{constants.TABULATED_MESSAGES_TABLE_NAME}"
    authors_missing_month_posts = (
        f"{bigquery_dataset}.{constants.DATA_QUALITY_MISSING_AUTHOR_POSTS_TABLE_NAME}"
    )

    data_quality_query = f"""
    CREATE OR REPLACE TABLE `{authors_missing_month_posts}` AS
    WITH authors AS (
    SELECT DISTINCT
        post_author_id,
        post_author_name_pi,
        post_author_link_pi
    FROM `{tabulate_table_name}`
    ),
    months AS (
        SELECT
            EXTRACT(YEAR FROM month) AS post_year,
            EXTRACT(MONTH FROM month) AS post_month
        FROM (
            SELECT GENERATE_DATE_ARRAY(
                DATE_TRUNC(CAST(MIN(post_date) AS DATE), MONTH),
                DATE_TRUNC(CAST(MAX(post_date) AS DATE), MONTH),
                INTERVAL 1 MONTH
            ) AS month_array
            FROM `{tabulate_table_name}`
        ),
        UNNEST(month_array) AS month
    ),
    all_possible_author_months AS (
        SELECT
            a.post_author_id,
            a.post_author_name_pi,
            a.post_author_link_pi,
            m.post_year,
            m.post_month
        FROM authors a
        CROSS JOIN months m
    ),
    existing_author_months AS (
        SELECT DISTINCT
            post_author_id,
            EXTRACT(YEAR FROM post_date) AS post_year,
            EXTRACT(MONTH FROM post_date) AS post_month
        FROM `{tabulate_table_name}`
    )
    SELECT
        apam.post_author_id,
        apam.post_author_name_pi,
        apam.post_author_link_pi,
        apam.post_year,
        apam.post_month
    FROM all_possible_author_months apam
    LEFT JOIN existing_author_months eam
        ON apam.post_author_id = eam.post_author_id
        AND apam.post_year = eam.post_year
        AND apam.post_month = eam.post_month
    WHERE eam.post_author_id IS NULL;
    """

    data_quality_job = client.query(data_quality_query)
    data_quality_job.result()


@prefect.task
def run_quality_checks(bigquery_dataset: str) -> None:
    """Runs all quality checks on the tabulated dataset.

    Parameters
        bigquery_dataset : str. The BigQuery dataset to use.
    """
    find_post_author_gaps(bigquery_dataset)
    # Add more quality checks here
