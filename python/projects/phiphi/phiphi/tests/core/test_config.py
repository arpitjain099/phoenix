"""Test config."""
import os
from unittest import mock

import dotenv

from phiphi.core import config

TEST_ENV_FILE = "tests/core/test_config.environment"


# Need to clear the environment or the values will be overwritten in the envfile
@mock.patch.dict(os.environ, {}, clear=True)
def test_settings():
    """Test the settings."""
    expected_config = dotenv.dotenv_values(TEST_ENV_FILE)
    settings = config.Settings(_env_file=TEST_ENV_FILE)  # type: ignore [call-arg]

    assert expected_config == settings.model_dump()
