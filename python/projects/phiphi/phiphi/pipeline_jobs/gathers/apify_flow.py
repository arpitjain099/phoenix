"""Flow for gathering data from Apify.

Single flow that all Apify scrapers use.

Includes switch for using mock data read directly from file for testing purposes.
"""
import json
from typing import Dict, Iterator, List, Tuple

import apify_client
import prefect

from phiphi import config
from phiphi.pipeline_jobs.gathers import apify_input_schemas, utils

input_actor_map = {
    apify_input_schemas.ApifyFacebookPostsInput: "apify/facebook-posts-scraper",
    apify_input_schemas.ApifyFacebookCommentsInput: "apify/facebook-comments-scraper",
    apify_input_schemas.TikTokScraperInput: "clockworks/tiktok-scraper",
    apify_input_schemas.TikTokCommentsScraperInput: "clockworks/tiktok-comments-scraper",
}


def apify_scrape(
    apify_token: str,
    actor_name: str,
    run_input: apify_input_schemas.ApifyInputType,
) -> Tuple[Iterator[Dict], apify_client.clients.DatasetClient]:
    """Scrape data using the Apify API and return an iterator."""
    client = apify_client.ApifyClient(apify_token)
    # Run the Apify actor
    run_info = client.actor(actor_name).call(run_input=run_input.dict(by_alias=True))
    assert run_info is not None
    # Access the dataset client associated with the actor's results
    dataset_client = client.dataset(run_info["defaultDatasetId"])
    return dataset_client.iterate_items(), dataset_client


def mock_apify_scrape(
    apify_token: str,
    actor_name: str,
    run_input: apify_input_schemas.ApifyInputType,
) -> Tuple[Iterator[Dict], None]:
    """Read mock scraping data and return an iterator."""
    if actor_name == "apify/facebook-posts-scraper":
        return iter(
            utils.load_sample_raw_data(
                source="apify",
                platform="facebook",
                data_type="post",
            )
        ), None
    else:
        raise NotImplementedError(f"Mock data not implemented for actor: {actor_name}")


@prefect.task
def apify_scrape_and_batch_download_results(
    apify_token: str,
    run_input: apify_input_schemas.ApifyInputType,
    batch_size: int = 100,
    dev_batch_dir: str = "",
) -> None:
    """Scrape data using the Apify API and save them to JSON blobs in batches."""
    apify_actor_name = input_actor_map[type(run_input)]

    if config.settings.USE_MOCK_APIFY:
        dataset_iterator, dataset_client = mock_apify_scrape(
            apify_token, apify_actor_name, run_input
        )
    else:
        dataset_iterator, dataset_client = apify_scrape(apify_token, apify_actor_name, run_input)

    # Initialize batch tracking
    batch_num = 1
    batch_items: List[Dict] = []

    # Iterate over dataset items and write to JSON files in batches
    for item in dataset_iterator:
        batch_items.append(item)

        # Write the batch to file when reaching the batch size
        if len(batch_items) == batch_size:
            file_name = dev_batch_dir + f"batch_{batch_num}.json"
            with open(file_name, "w") as f:
                json.dump(batch_items, f)

            batch_items.clear()
            batch_num += 1

    # Write any remaining items in the final batch if not empty
    if batch_items:
        file_name = dev_batch_dir + f"batch_{batch_num}.json"
        with open(file_name, "w") as f:
            json.dump(batch_items, f)

    # Delete the dataset after downloading to save on storage costs
    if dataset_client is not None:
        dataset_client.delete()

    prefect.get_run_logger().info(f"Finished scraping. Batches written: {batch_num}")
