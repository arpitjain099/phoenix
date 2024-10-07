"""Module containing the Prefect flow for tabulate."""
from typing import Coroutine

import prefect
from google.cloud import bigquery

from phiphi import constants
from phiphi.pipeline_jobs import constants as pipeline_jobs_constants


def escape_sql_value(value: str) -> str:
    """Escapes single quotes in a string for safe SQL queries."""
    return value.replace("'", "\\'")


@prefect.task
def tabulate(
    job_run_id: int,
    bigquery_dataset: str,
    classifiers_dict_list: list[dict],
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
    manually_classified_authors_table_name = (
        f"{bigquery_dataset}.{pipeline_jobs_constants.MANUALLY_CLASSIFIED_AUTHORS_TABLE_NAME}"
    )

    # Note, we could convert the classifier dicts into their pydantic models, and then get type
    # checking on `id` and `version_id`, but this makes testing harder as we need to create entire
    # classifier objects instead of just minimal dicts.
    # Note we always add `(NULL, NULL)` to handle the case where there are no classifiers.
    classifier_ids = ", ".join(
        ["(NULL, NULL)"]
        + [f"({d['id']}, {d['latest_version']['version_id']})" for d in classifiers_dict_list]
    )

    tabulate_query = f"""
    CREATE OR REPLACE TABLE `{tabulate_table_name}` AS
    WITH active_only_classified_messages AS (
        SELECT *
        FROM `{classified_messages_table_name}`
        WHERE (classifier_id, classifier_version_id) IN ({classifier_ids})
    ),
    messages_classes AS (
        SELECT
            m.*,
            cm.class_name AS class,
            mca.class_name AS author_class_name,
        FROM
            `{source_table_name}` m
        LEFT JOIN
            active_only_classified_messages cm
        ON
            m.phoenix_platform_message_id = cm.phoenix_platform_message_id
        LEFT JOIN
            `{manually_classified_authors_table_name}` mca
        ON
            m.phoenix_platform_message_author_id = mca.phoenix_platform_author_id
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
        -- Currently many columns not implemented (i.e. NULL)
        CAST(NULL AS STRING) AS post_author_category,
        p.author_class_name AS post_author_class,
        CAST(NULL AS STRING) AS post_author_description_pi,
        CAST(NULL AS INT64) AS post_author_followers_count,
        p.phoenix_platform_message_author_id AS post_author_id,
        CAST(NULL AS STRING) AS post_author_location,
        p.pi_platform_message_author_name AS post_author_name_pi,
        CAST(NULL AS STRING) AS post_author_link_pi,

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
        c.author_class_name AS comment_author_class,
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
        CAST(NULL AS INT64) AS facebook_video_views,
        -- TikTok
        CAST(NULL AS INT64) AS tiktok_post_plays,
        -- X
        CAST(NULL AS INT64) AS x_tweet_quotes,

        -- Developer fields should always be last
        -- Using CURRENT_TIMESTAMP rather then PARSE_TIMESTAMP as it seems to make the integration
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
    classifiers_dict_list: list[dict],
) -> None:
    """Flow which tabulates data - producing the dataset for the dashboard to use."""
    tabulate(
        job_run_id=job_run_id,
        bigquery_dataset=project_namespace,
        classifiers_dict_list=classifiers_dict_list,
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
