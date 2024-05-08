"""Flow for gathering data from Apify.

Single flow that all Apify scrapers use.
"""
import json
from typing import Dict, List, Literal, Union

import prefect
from apify_client import ApifyClient
from phiphi.pipeline_jobs.gathers import schemas


@prefect.task
def trigger_apify_scrape_and_batch_download_results(
    apify_token: str,
    data_type: Literal["posts", "comments"],
    run_input: Union[schemas.ApifyFacebookPostsInput],
    batch_size: int = 100,
) -> None:
    """Scrape data using the Apify API and save them to JSON blobs in batches."""
    apify_client = ApifyClient(apify_token)

    # Start the Apify actor
    run_info = apify_client.actor("apify/facebook-posts-scraper").call(
        run_input=run_input.dict(by_alias=True)
    )

    assert run_info is not None

    # Access the dataset client associated with the actor's results
    dataset_client = apify_client.dataset(run_info["defaultDatasetId"])

    # Initialize batch tracking
    batch_num = 1
    batch_items: List[Dict] = []

    # Iterate over dataset items and write to JSON files in batches
    for item in dataset_client.iterate_items():
        batch_items.append(item)

        # Write the batch to file when reaching the batch size
        if len(batch_items) == batch_size:
            file_name = f"batch_{batch_num}.json"
            with open(file_name, "w") as f:
                json.dump(batch_items, f)

            batch_items.clear()
            batch_num += 1

    # Write any remaining items in the final batch if not empty
    if batch_items:
        file_name = f"batch_{batch_num}.json"
        with open(file_name, "w") as f:
            json.dump(batch_items, f)

    # Delete the dataset after downloading to save on storage costs
    dataset_client.delete()

    prefect.get_run_logger().info(f"Finished scraping. Batches written: {batch_num}")
