"""Utils for gathers."""
import json
import pathlib
from typing import Literal


def load_sample_raw_data(
    source: Literal["apify"],
    platform: Literal["facebook", "instagram", "tiktok", "x-twitter"],
    data_type: Literal["post", "comment"],
) -> list[dict]:
    """Return a sample raw data JSON blob for a given source, platform, and data type."""
    if source == "apify" and platform == "facebook" and data_type == "post":
        relative_path = "sample_apify_data/facebook_posts.json"
    else:
        raise NotImplementedError(f"{source=}, {platform=}, {data_type=} not supported.")

    base_path = pathlib.Path(__file__).parent
    full_path = base_path.joinpath(relative_path).resolve()
    with open(full_path, "r") as f:
        data: list[dict] = json.load(f)
    return data
