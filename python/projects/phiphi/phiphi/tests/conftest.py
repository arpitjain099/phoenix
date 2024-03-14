"""Conftest."""
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from phiphi import main
from phiphi.core import config, db
from phiphi.seed import main as seed_main


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="function")
def reseed_tables(session):
    """Reseed the tables.

    Use this fixture to reset the data for a test.
    """
    db.Base.metadata.drop_all(bind=session.get_bind())
    db.Base.metadata.create_all(bind=session.get_bind())
    seed_main.main(session, testing=True)
    yield session
