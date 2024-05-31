"""Utils for gathers."""
import json
import pathlib

from phiphi.api.projects.gathers import schemas as gather_schemas


def load_sample_raw_data(
    source: gather_schemas.Source,
    platform: gather_schemas.Platform,
    data_type: gather_schemas.DataType,
) -> list[dict]:
    """Return a sample raw data JSON blob for a given source, platform, and data type."""
    if (
        source == gather_schemas.Source.apify
        and platform == gather_schemas.Platform.facebook
        and data_type == gather_schemas.DataType.posts
    ):
        relative_path = "apify_sample_data/facebook_posts.json"
    else:
        raise NotImplementedError(f"{source=}, {platform=}, {data_type=} not supported.")

    base_path = pathlib.Path(__file__).parent
    full_path = base_path.joinpath(relative_path).resolve()
    with open(full_path, "r") as f:
        data: list[dict] = json.load(f)
    return data
