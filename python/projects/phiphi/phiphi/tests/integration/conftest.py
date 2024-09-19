"""Common fixtures for integration tests."""
import uuid

import pytest

from phiphi.pipeline_jobs import projects


@pytest.fixture
def tmp_project_namespace():
    """Generate a temporary project namespace for testing."""
    tmp_project_namespace_hash = str(uuid.uuid4())[:10]
    tmp_project_namespace_hash = tmp_project_namespace_hash.replace("-", "")
    return f"test_{tmp_project_namespace_hash}"


@pytest.fixture
def tmp_bq_project(tmp_project_namespace):
    """Setup and breakdown of a test project namespace wrapper for integration tests."""
    print(f"Test project namespace: {tmp_project_namespace}")
    projects.init_project_db.fn(tmp_project_namespace, with_dummy_data=True)

    yield tmp_project_namespace

    projects.delete_project_db.fn(tmp_project_namespace)
