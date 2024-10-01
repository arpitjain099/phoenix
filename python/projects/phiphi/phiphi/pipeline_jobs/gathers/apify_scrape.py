"""Flow for gathering data from Apify.

Single flow that all Apify scrapers use.

Includes switch for using mock data read directly from file for testing purposes.
"""
import json
import logging
from datetime import datetime
from typing import Dict, Iterator, List, Tuple

import apify_client
import pandas as pd
import prefect

from phiphi import config, utils
from phiphi.api.projects import gathers
from phiphi.pipeline_jobs import constants, gather_batches
from phiphi.pipeline_jobs import utils as pipeline_jobs_utils
from phiphi.pipeline_jobs.gathers import types as gather_types
from phiphi.pipeline_jobs.gathers import utils as gather_utils

gather_apify_actor_map: dict[type[gathers.schemas.GatherResponse], str] = {
    gathers.apify_facebook_posts.schemas.ApifyFacebookPostsGatherResponse: (
        "apify/facebook-posts-scraper"
    ),
    gathers.apify_facebook_comments.schemas.ApifyFacebookCommentsGatherResponse: (
        "apify/facebook-comments-scraper"
    ),
    gathers.apify_tiktok_accounts_posts.schemas.ApifyTikTokAccountsPostsGatherResponse: (
        "clockworks/tiktok-scraper"
    ),
    gathers.apify_tiktok_hashtags_posts.schemas.ApifyTikTokHashtagsPostsGatherResponse: (
        "clockworks/tiktok-scraper"
    ),
    gathers.apify_tiktok_searches_posts.schemas.ApifyTikTokSearchesPostsGatherResponse: (
        "clockworks/tiktok-scraper"
    ),
    gathers.apify_tiktok_comments.schemas.ApifyTikTokCommentsGatherResponse: (
        "apidojo/tiktok-comments-scraper"
    ),
}


def apify_scrape(
    apify_token: str,
    actor_name: str,
    gather: gathers.schemas.GatherResponse,
    logger: None | logging.Logger | logging.LoggerAdapter = None,
) -> Tuple[Iterator[Dict], apify_client.clients.DatasetClient]:
    """Scrape data using the Apify API and return an iterator."""
    client = apify_client.ApifyClient(apify_token)
    # Run the Apify actor
    run_info = client.actor(actor_name).call(run_input=gather.serialize_to_apify_input())
    if logger is not None:
        logger.info("Apify actor run info returned from call:")
        logger.info(run_info)
    assert run_info is not None
    # Access the dataset client associated with the actor's results
    dataset_client = client.dataset(run_info["defaultDatasetId"])
    return dataset_client.iterate_items(), dataset_client


def mock_apify_scrape(
    apify_token: str,
    actor_name: str,
    gather: gathers.schemas.GatherResponse,
) -> Tuple[Iterator[Dict], None]:
    """Read mock scraping data and return an iterator."""
    return iter(
        gather_utils.load_sample_raw_data(
            child_type_name=gather.child_type,
        )
    ), None


def update_and_write_batch(
    batch_id: int,
    batch_items: List[Dict],
    gather_batch_df: pd.DataFrame,
    bigquery_dataset: str,
    bigquery_table: str,
) -> None:
    """Update the gathered_at and json_data fields and write."""
    # Update the specific columns
    gather_batch_df.loc[0, "batch_id"] = batch_id
    gather_batch_df.loc[0, "gathered_at"] = datetime.utcnow()
    gather_batch_df.loc[0, "json_data"] = json.dumps(batch_items)

    # Validate the DataFrame against the Pandera schema
    validated_df = gather_batches.gather_batches_schema.validate(gather_batch_df)

    pipeline_jobs_utils.write_data(df=validated_df, dataset=bigquery_dataset, table=bigquery_table)


@prefect.task
def apify_scrape_and_batch_download_results(
    gather: gathers.schemas.GatherResponse,
    job_run_id: int,
    bigquery_dataset: str,
    bigquery_table: str = constants.GATHER_BATCHES_TABLE_NAME,
    batch_size: int = constants.DEFAULT_BATCH_SIZE,
) -> gather_types.ScrapeResponse:
    """Scrape data using the Apify API and save them to a GCP BigQuery table or Parquet."""
    prefect_logger = prefect.get_run_logger()

    apify_token = utils.get_apify_api_key()
    apify_actor_name = gather_apify_actor_map[type(gather)]

    if config.settings.USE_MOCK_APIFY:
        prefect_logger.info("Reading mock data.")
        dataset_iterator, dataset_client = mock_apify_scrape(apify_token, apify_actor_name, gather)
    else:
        prefect_logger.info("Making Apify call.")
        dataset_iterator, dataset_client = apify_scrape(
            apify_token, apify_actor_name, gather, prefect_logger
        )

    # Initialize batch tracking
    item_count = 0
    batch_num = 0
    batch_items: List[Dict] = []

    gather_creation_defaults = gathers.child_types.get_gather_project_db_defaults(
        gather.child_type
    )

    static_data = {
        "gather_id": gather.id,
        "job_run_id": job_run_id,
        "gather_type": gather.child_type,
        "platform": gather_creation_defaults.platform,
        "data_type": gather_creation_defaults.data_type,
        "batch_id": 0,  # This will be updated for each batch
        "gathered_at": datetime.utcnow(),  # This will be updated for each batch
        "json_data": "",  # This will be updated for each batch
        "last_processed_at": pd.NaT,  # Use pd.NaT for missing datetime values
    }

    gather_batch_df = pd.DataFrame([static_data])
    gather_batch_df["last_processed_at"] = gather_batch_df["last_processed_at"].dt.tz_localize(
        "UTC"
    )
    validated_gather_batch_df = gather_batches.gather_batches_schema.validate(gather_batch_df)

    # Iterate over dataset items and insert into BigQuery or Parquet in batches
    for item in dataset_iterator:
        item_count += 1
        batch_items.append(item)

        # Insert the batch into BigQuery or Parquet when reaching the batch size
        if len(batch_items) == batch_size:
            prefect_logger.info(f"Inserting batch {batch_num}")
            update_and_write_batch(
                batch_num,
                batch_items,
                validated_gather_batch_df,
                bigquery_dataset,
                bigquery_table,
            )
            batch_items.clear()
            batch_num += 1

    # Insert any remaining items in the final batch if not empty
    if batch_items:
        prefect_logger.info(f"Inserting final batch {batch_num}")
        update_and_write_batch(
            batch_num,
            batch_items,
            validated_gather_batch_df,
            bigquery_dataset,
            bigquery_table,
        )
        # Add a batch number if there are items in the final batch
        batch_num += 1

    # Delete the dataset after downloading to save on storage costs
    if dataset_client is not None:
        dataset_client.delete()

    prefect_logger.info("Finished scraping.")
    prefect_logger.info(f"Batches inserted: {batch_num}.")
    prefect_logger.info(f"Items scraped: {item_count}.")
    return gather_types.ScrapeResponse(total_items=item_count, total_batches=batch_num)
