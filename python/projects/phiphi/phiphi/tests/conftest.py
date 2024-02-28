"""Conftest for phiphi/tests/."""
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from phiphi.main import app


@pytest.fixture(scope="module")
def client() -> Generator:
    """Create a client for testing."""
    with TestClient(app) as c:
        yield c
