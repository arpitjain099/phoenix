"""Flow for gathering data from Apify.

Single flow that all Apify scrapers use.

Includes switch for using mock data read directly from file for testing purposes.
"""
import json
from typing import Dict, Iterator, List, Tuple

import apify_client
import pandas as pd
import prefect

from phiphi import config, utils
from phiphi.api.projects import gathers
from phiphi.pipeline_jobs import utils as pipeline_jobs_utils
from phiphi.pipeline_jobs.gathers import (
    apify_input_schemas,
    constants,
    project_db_schemas,
)
from phiphi.pipeline_jobs.gathers import utils as gather_utils

input_actor_map = {
    gathers.apify_facebook_posts.schemas.ApifyFacebookPostGatherResponse: (
        "apify/facebook-posts-scraper"
    ),
    gathers.apify_facebook_comments.schemas.ApifyFacebookCommentGatherResponse: (
        "apify/facebook-comments-scraper"
    ),
    apify_input_schemas.ApifyTiktokPostsInput: "clockworks/tiktok-scraper",
    apify_input_schemas.ApifyTiktokCommentsInput: "clockworks/tiktok-comments-scraper",
}


def apify_scrape(
    apify_token: str,
    actor_name: str,
    run_input: gathers.schemas.GatherResponse,
) -> Tuple[Iterator[Dict], apify_client.clients.DatasetClient]:
    """Scrape data using the Apify API and return an iterator."""
    client = apify_client.ApifyClient(apify_token)
    # Run the Apify actor
    run_info = client.actor(actor_name).call(run_input=run_input.serialize_to_apify_input())
    assert run_info is not None
    # Access the dataset client associated with the actor's results
    dataset_client = client.dataset(run_info["defaultDatasetId"])
    return dataset_client.iterate_items(), dataset_client


def mock_apify_scrape(
    apify_token: str,
    actor_name: str,
    run_input: gathers.schemas.GatherResponse,
) -> Tuple[Iterator[Dict], None]:
    """Read mock scraping data and return an iterator."""
    return iter(
        gather_utils.load_sample_raw_data(
            source=gathers.schemas.Source.apify,
            platform=run_input.platform,
            data_type=run_input.data_type,
        )
    ), None


def update_and_write_batch(
    batch_id: int,
    batch_items: List[Dict],
    gather_batch_df: pd.DataFrame,
    bigquery_dataset: str,
    bigquery_table: str,
) -> None:
    """Update the batch_created_at and json_data fields and write."""
    # Update the specific columns
    gather_batch_df.loc[0, "batch_id"] = batch_id
    gather_batch_df.loc[0, "batch_created_at"] = pd.Timestamp.now()
    gather_batch_df.loc[0, "json_data"] = json.dumps(batch_items)

    # Validate the DataFrame against the Pandera schema
    validated_df = project_db_schemas.gather_batches_schema.validate(gather_batch_df)

    pipeline_jobs_utils.write_data(df=validated_df, dataset=bigquery_dataset, table=bigquery_table)


@prefect.task
def apify_scrape_and_batch_download_results(
    run_input: gathers.schemas.GatherResponse,
    project_id: int,
    gather_id: int,
    job_run_id: int,
    bigquery_dataset: str,
    bigquery_table: str = constants.GATHER_BATCHES_TABLE_NAME,
    batch_size: int = 100,
) -> None:
    """Scrape data using the Apify API and save them to a GCP BigQuery table or Parquet."""
    prefect_logger = prefect.get_run_logger()

    apify_token = utils.get_apify_api_key()
    apify_actor_name = input_actor_map[type(run_input)]

    if config.settings.USE_MOCK_APIFY:
        prefect_logger.info("Reading mock data.")
        dataset_iterator, dataset_client = mock_apify_scrape(
            apify_token, apify_actor_name, run_input
        )
    else:
        prefect_logger.info("Making Apify call.")
        dataset_iterator, dataset_client = apify_scrape(apify_token, apify_actor_name, run_input)

    # Initialize batch tracking
    batch_num = 0
    batch_items: List[Dict] = []

    static_data = {
        "project_id": project_id,
        "gather_id": gather_id,
        "job_run_id": job_run_id,
        "source": "apify",
        "platform": run_input.platform,
        "data_type": run_input.data_type,
        "batch_id": 0,  # This will be updated for each batch
        "batch_created_at": pd.Timestamp.now(),  # This will be updated for each batch
        "json_data": "",  # This will be updated for each batch
        "last_processed_at": pd.NaT,  # Use pd.NaT for missing datetime values
    }

    gather_batch_df = pd.DataFrame([static_data])
    project_db_schemas.gather_batches_schema.validate(gather_batch_df)

    # Iterate over dataset items and insert into BigQuery or Parquet in batches
    for item in dataset_iterator:
        batch_items.append(item)

        # Insert the batch into BigQuery or Parquet when reaching the batch size
        if len(batch_items) == batch_size:
            prefect_logger.info(f"Inserting batch {batch_num}")
            update_and_write_batch(
                batch_num,
                batch_items,
                gather_batch_df,
                bigquery_dataset,
                bigquery_table,
            )
            batch_items.clear()
            batch_num += 1

    # Insert any remaining items in the final batch if not empty
    if batch_items:
        update_and_write_batch(
            batch_num,
            batch_items,
            gather_batch_df,
            bigquery_dataset,
            bigquery_table,
        )
        batch_num += 1
        prefect_logger.info(f"Inserting final batch {batch_num}")

    # Delete the dataset after downloading to save on storage costs
    if dataset_client is not None:
        dataset_client.delete()

    prefect_logger.info(f"Finished scraping. Batches inserted: {batch_num}")
