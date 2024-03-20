"""Conftest."""
from typing import Generator, Iterator

import pydantic_core
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from phiphi.api import main
from phiphi.core import config, db
from phiphi.seed import main as seed_main


#  If this fixture is not in a test it can lead to unexpected errors as the app will use the
#  production database rather then the test.
@pytest.fixture(scope="session", autouse=True)
def test_app(session) -> Generator[main.FastAPI, None, None]:
    """Initialise the test app.

    Includes overriding the get_session dependency to use the session fixture. This is necessary to
    use the test sessions in the app.
    """

    def override_get_session():
        yield session

    main.app.dependency_overrides[db.get_session] = override_get_session
    yield main.app


@pytest.fixture(scope="session")
def client(test_app) -> Generator[TestClient, None, None]:
    """Client for testing."""
    with TestClient(test_app) as client:
        yield client


@pytest.fixture(scope="session")
def client_first_admin_user(test_app) -> Generator[TestClient, None, None]:
    """Client for testing authenticated with first admin user."""
    with TestClient(
        test_app,
        headers={config.settings.HEADER_AUTH_NAME: config.settings.FIRST_ADMIN_USER_EMAIL},
    ) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def test_engine():
    """Create a test engine for the database."""
    engine = create_engine(str(config.settings.TESTING_SQLALCHEMY_DATABASE_URI))
    return engine


@pytest.fixture(scope="session")
def session(test_engine) -> Generator[Session, None, None]:
    """Create the session for testing."""
    with Session(test_engine) as session:
        yield session


@pytest.fixture(scope="function")
def recreate_tables(session):
    """Recreate tables deleting all the data in the database.

    Use this fixture to reset the data for a test.
    """
    db.Base.metadata.drop_all(bind=session.get_bind())
    db.Base.metadata.create_all(bind=session.get_bind())
    yield session
    # Need to close the session or will not release the lock on the database
    # and next command in an other connection will hang.
    session.close()


@pytest.fixture(scope="function")
def reseed_tables(session):
    """Reseed the tables.

    Use this fixture to reset the data for a test.
    """
    db.Base.metadata.drop_all(bind=session.get_bind())
    db.Base.metadata.create_all(bind=session.get_bind())
    seed_main.main(session, testing=True)
    yield session
    # Need to close the session or will not release the lock on the database
    # and next command in an other connection will hang.
    session.close()


@pytest.fixture(scope="function")
def patch_settings(request: pytest.FixtureRequest) -> Iterator[config.Settings]:
    """Patch the settings with given variables.

    Use this fixture to patch config.settings with the different values. The values are passed
    as a dictionary in the patch_settings decorator. Any settings that are not set via the
    dictionary will be set to the default value.

    Taken from:
    https://rednafi.com/python/patch_pydantic_settings_in_pytest/

    There where a few changes to the original code to make it work with the linting and versions in
    this project.

    Example:
    @pytest.mark.patch_settings(
        {"USE_COOKIE_AUTH": False, "COOKIE_AUTH_NAME": COOKIE_AUTH_TEST_NAME}
    )
    def test_something(patch_settings):
        pass
    """
    # Make a copy of the original settings
    original_settings = config.settings.model_copy()

    # Collect the values to patch
    marker = request.node.get_closest_marker("patch_settings")
    if marker is None:
        env_vars_to_patch = {}
    else:
        env_vars_to_patch = marker.args[0]

    # Patch the settings to use the default values
    for k, v in config.settings.model_fields.items():
        if v.default is not pydantic_core.PydanticUndefined:
            setattr(config.settings, k, v.default)

    for key, val in env_vars_to_patch.items():
        # Raise an error if the patch settings is not defined in the settings
        if not hasattr(config.settings, key):
            raise ValueError(f"Unknown setting: {key}")

        setattr(config.settings, key, val)

    yield config.settings
    # Restore the original settings
    config.settings.__dict__.update(original_settings.__dict__)
