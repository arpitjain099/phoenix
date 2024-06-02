"""Utils for phiphi."""
from phiphi import config

BIGQUERY_DATASET_NAME_FOR_PROJECT = "project_id{project_id}"


def get_apify_api_key(environment_slug: str | None = None) -> str:
    """Get the apify api key for the environment."""
    if not environment_slug:
        environment_slug = config.settings.FIRST_ENVIRONMENT_SLUG
    if environment_slug not in config.settings.APIFY_API_KEYS:
        raise ValueError(f"No apify api key found for environment: {environment_slug}")
    return config.settings.APIFY_API_KEYS[environment_slug]


def get_bigquery_dataset_name(project_id: int) -> str:
    """Get the bigquery dataset name."""
    return BIGQUERY_DATASET_NAME_FOR_PROJECT.format(
        project_id=project_id
    )
