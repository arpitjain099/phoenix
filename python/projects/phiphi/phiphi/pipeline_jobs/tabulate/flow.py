"""Module containing the Prefect flow for tabulate."""
from typing import Coroutine

import prefect
from google.cloud import bigquery

from phiphi import constants
from phiphi.pipeline_jobs import constants as pipeline_jobs_constants


@prefect.task
def tabulate(
    job_run_id: int,
    bigquery_dataset: str,
    class_id_name_map: dict[int, str],
) -> None:
    """Task which tabulates data.

    The tabulate flow must produce a table that matches the schema the file `tabulated_messages.py`
    and in the notion manual.
    TODO: add link to notion once if become stable/deployed so it is one URL rather then versioned.
    """
    client = bigquery.Client()

    source_table_name = f"{bigquery_dataset}.{pipeline_jobs_constants.DEDUPLICATED_GENERALISED_MESSAGES_TABLE_NAME}"  # noqa: E501
    tabulate_table_name = (
        f"{bigquery_dataset}.{pipeline_jobs_constants.TABULATED_MESSAGES_TABLE_NAME}"
    )
    classified_messages_table_name = (
        f"{bigquery_dataset}.{pipeline_jobs_constants.CLASSIFIED_MESSAGES_TABLE_NAME}"
    )

    if class_id_name_map:
        # Generate the CASE statement for class names mapping from their IDs
        class_name_case_statements = [
            f"WHEN cm.class_id = {class_id} THEN '{class_name}'"
            for class_id, class_name in class_id_name_map.items()
        ]
        class_name_case_statement_sql = (
            "CASE "
            + " ".join(class_name_case_statements)
            + " WHEN cm.class_id IS NULL THEN NULL"
            + " ELSE 'missing_class_name' END AS class"
        )
    else:
        class_name_case_statement_sql = "NULL AS class"

    tabulate_query = f"""
    CREATE OR REPLACE TABLE `{tabulate_table_name}` AS
    WITH messages_classes AS (
        SELECT
            m.*,
            {class_name_case_statement_sql}
        FROM
            `{source_table_name}` m
        LEFT JOIN
            `{classified_messages_table_name}` cm
        ON
            m.phoenix_platform_message_id = cm.phoenix_platform_message_id
    ),
    posts AS (
        SELECT
            *
        FROM
            messages_classes
        WHERE
            data_type = 'posts'
    ),
    comments AS (
        SELECT
            *
        FROM
            messages_classes
        WHERE
            data_type = 'comments'
    )
    SELECT
        p.platform AS platform,

        -- Post Author
        -- Currently no implemented
        NULL AS post_author_category,
        NULL AS post_author_class,
        NULL AS post_author_description,
        NULL AS post_author_followers,
        p.phoenix_platform_message_author_id AS post_author_id,
        NULL AS post_author_location,
        p.pi_platform_message_author_name AS post_author_name_pi,
        NULL AS post_author_link_pi,

        -- Post
        p.class AS post_class,
        p.comment_count AS post_comment_count,
        p.platform_message_last_updated_at AS post_date,
        p.gather_id AS post_gather_id,
        p.phoenix_platform_message_id AS post_id,
        p.like_count AS post_like_count,
        p.pi_platform_message_url AS post_link_pi,
        p.share_count AS post_share_count,
        p.pi_text AS post_text_pi,

        -- Comment Author
        NULL AS comment_author_class,
        c.phoenix_platform_message_author_id AS comment_author_id,
        c.pi_platform_message_author_name AS comment_author_name_pi,

        -- Comment
        c.class AS comment_class,
        c.platform_message_last_updated_at AS comment_date,
        c.gather_id AS comment_gather_id,
        c.phoenix_platform_message_id AS comment_id,
        c.like_count AS comment_like_count,
        c.pi_platform_message_url AS comment_link_pi,
        c.phoenix_platform_root_message_id AS comment_parent_post_id,
        c.phoenix_platform_parent_message_id AS comment_replied_to_id,
        c.pi_text AS comment_text_pi,

        -- Platform specific stats
        -- Facebook
        NULL AS facebook_video_views,
        -- TikTok
        NULL AS tiktok_post_plays,

        -- Developer fields should always be last
        -- Using CURRENT_TIMESTAMP rather then PARSE_TIMESTAMPE as it seems to make the integration
        -- tests faster.
        CURRENT_TIMESTAMP() AS phoenix_processed_at,
        {job_run_id} AS phoenix_job_run_id
    FROM
        posts p
    LEFT JOIN
        comments c
    ON
        p.phoenix_platform_message_id = c.phoenix_platform_root_message_id
    """

    tabulate_job = client.query(tabulate_query)
    tabulate_job.result()


@prefect.flow(name="tabulate_flow")
def tabulate_flow(
    job_run_id: int,
    project_namespace: str,
    class_id_name_map: dict[int, str],
) -> None:
    """Flow which tabulates data - producing the dataset for the dashboard to use."""
    tabulate(
        job_run_id=job_run_id,
        bigquery_dataset=project_namespace,
        class_id_name_map=class_id_name_map,
    )


def create_deployments(
    override_work_pool_name: str | None = None,
    deployment_name_prefix: str = "",
    image: str = constants.DEFAULT_IMAGE,
    tags: list[str] = [],
    build: bool = False,
    push: bool = False,
) -> list[Coroutine]:
    """Create deployments for flow_runner_flow.

    Args:
        override_work_pool_name (str | None): The name of the work pool to use to override the
        default work pool.
        deployment_name_prefix (str, optional): The prefix of the deployment name. Defaults to "".
        image (str, optional): The image to use for the deployments. Defaults to
        constants.DEFAULT_IMAGE.
        tags (list[str], optional): The tags to use for the deployments. Defaults to [].
        build (bool, optional): If True, build the image. Defaults to False.
        push (bool, optional): If True, push the image. Defaults to False.

    Returns:
        list[Coroutine]: List of coroutines that create deployments.
    """
    work_pool_name = str(constants.WorkPool.main)
    if override_work_pool_name:
        work_pool_name = override_work_pool_name
    task = tabulate_flow.deploy(
        name=deployment_name_prefix + tabulate_flow.name,
        work_pool_name=work_pool_name,
        image=image,
        build=build,
        push=push,
        tags=tags,
    )

    return [task]
