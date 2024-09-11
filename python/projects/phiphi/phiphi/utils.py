"""Utils for phiphi."""
import json
import logging
import os
import re

import sentry_sdk
import yaml
from google import auth

from phiphi import config

PROJECT_NAMESPACE_STRING = "project_id{project_id}"


def get_apify_api_key(workspace_slug: str | None = None) -> str:
    """Get the apify api key for the workspace."""
    if config.settings.USE_MOCK_APIFY:
        return "mock_apify_api_key"
    if not workspace_slug:
        workspace_slug = config.settings.FIRST_WORKSPACE_SLUG
    if workspace_slug not in config.settings.APIFY_API_KEYS:
        raise ValueError(f"No apify api key found for workspace: {workspace_slug}")
    return config.settings.APIFY_API_KEYS[workspace_slug]


def get_project_namespace(project_id: int, namespace_prefix: str = "") -> str:
    """Get the project namespace.

    The project name is a unique identifier for the project.
    It can be used for  naming resources like bigquery datasets.

    The namespace must be a valid BigQuery dataset name. As such project_id and namespace_prefix
    must follow the constraints for BigQuery dataset names:
    https://cloud.google.com/bigquery/docs/datasets#dataset-naming

    Args:
        project_id (int): The project id.
        namespace_prefix (str, optional): The namespace prefix. Defaults to "".
            Used for testing.
    """
    namespace = namespace_prefix + PROJECT_NAMESPACE_STRING.format(project_id=project_id)
    if not is_valid_bigquery_dataset_name(namespace):
        raise ValueError(f"Invalid project namespace: {namespace}")
    return namespace


def is_valid_bigquery_dataset_name(dataset_name: str) -> bool:
    """Check if the provided string is a valid BigQuery dataset name.

    Args:
        dataset_name (str): The dataset name to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    # Check length constraint
    if len(dataset_name) > 1024:
        return False

    # Check allowed characters
    if not re.match(r"^[a-zA-Z0-9_]+$", dataset_name):
        return False

    return True


def init_logging(log_config: str | None = config.settings.PHIPHI_LOG_CONFIG) -> None:
    """Initialize logging with the provided configuration file."""
    if not log_config:
        return None

    if not os.path.exists(log_config):
        raise FileNotFoundError(f"Logging configuration file not found: {log_config}")

    if log_config.endswith(".yaml") or log_config.endswith(".yml"):
        with open(log_config, "r") as file:
            logging_config = yaml.safe_load(file)
        logging.config.dictConfig(logging_config)
    elif log_config.endswith(".json"):
        with open(log_config, "r") as file:
            logging_config = json.load(file)
        logging.config.dictConfig(logging_config)
    else:
        raise ValueError(f"Unsupported logging configuration file type: {log_config}")

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Using configuration file: {log_config}")


def init_sentry(
    dsn: str | None = config.settings.SENTRY_DSN,
    traces_sample_rate: float = config.settings.SENTRY_TRACES_SAMPLE_RATE,
    profiles_sample_rate: float = config.settings.SENTRY_PROFILES_SAMPLE_RATE,
    environment: str = config.settings.SENTRY_ENVIRONMENT,
    release: str = config.settings.VERSION,
) -> None:
    """Initialize sentry."""
    if dsn:
        sentry_sdk.init(
            dsn=dsn,
            traces_sample_rate=traces_sample_rate,
            profiles_sample_rate=profiles_sample_rate,
            environment=environment,
            release=release,
        )


def get_default_bigquery_project() -> str:
    """Get the default BigQuery project based on the current environment."""
    _, project = auth.default()
    # Cast needed for typing
    return str(project)
