"""Common fixtures for integration tests."""
import uuid

import pytest

from phiphi.pipeline_jobs import projects


@pytest.fixture
def tmp_bq_project():
    """Setup and breakdown of a test project namespace wrapper for integration tests."""
    temp_project_namespace = str(uuid.uuid4())[:10]
    temp_project_namespace = temp_project_namespace.replace("-", "")
    test_project_namespace = f"test_{temp_project_namespace}"
    print(f"Test project namespace: {test_project_namespace}")
    projects.init_project_db.fn(test_project_namespace, with_dummy_rows=2)

    yield test_project_namespace

    projects.delete_project_db.fn(test_project_namespace)
