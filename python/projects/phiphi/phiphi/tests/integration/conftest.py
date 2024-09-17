"""Common fixtures for integration tests."""
import uuid

import pytest

from phiphi.pipeline_jobs import projects


@pytest.fixture
def temp_project_namespace():
    """Generate a temporary project namespace for testing."""
    temp_project_namespace = str(uuid.uuid4())[:10]
    temp_project_namespace = temp_project_namespace.replace("-", "")
    return f"test_{temp_project_namespace}"


@pytest.fixture
def tmp_bq_project(temp_project_namespace):
    """Setup and breakdown of a test project namespace wrapper for integration tests."""
    print(f"Test project namespace: {temp_project_namespace}")
    projects.init_project_db.fn(temp_project_namespace, with_dummy_data=True)

    yield temp_project_namespace

    projects.delete_project_db.fn(temp_project_namespace)
