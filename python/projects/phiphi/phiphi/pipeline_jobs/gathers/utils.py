"""Utils for gathers."""
import json
import pathlib

from phiphi.api.projects.gathers import schemas as gather_schemas


def load_sample_raw_data(
    child_type_name: gather_schemas.ChildTypeName,
) -> list[dict]:
    """Return a sample raw data JSON blob for a given gather child type."""
    if child_type_name == gather_schemas.ChildTypeName.apify_facebook_posts:
        relative_path = "apify_sample_data/facebook_posts.json"
    elif child_type_name == gather_schemas.ChildTypeName.apify_facebook_comments:
        relative_path = "apify_sample_data/facebook_comments.json"
    else:
        raise NotImplementedError(f"{child_type_name=} not supported.")

    base_path = pathlib.Path(__file__).parent
    full_path = base_path.joinpath(relative_path).resolve()
    with open(full_path, "r") as f:
        data: list[dict] = json.load(f)
    return data
