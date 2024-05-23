"""Utils for phiphi."""
from phiphi import config


def get_apify_api_key(environment_slug: str | None = None) -> str:
    """Get the apify api key for the environment."""
    if not environment_slug:
        environment_slug = config.settings.FIRST_ENVIRONMENT_SLUG
    if environment_slug not in config.settings.APIFY_API_KEYS:
        raise ValueError(f"No apify api key found for environment: {environment_slug}")
    return config.settings.APIFY_API_KEYS[environment_slug]
