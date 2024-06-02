"""Integration tests for the data pipeline with big query."""
from google.cloud import bigquery

from phiphi.pipeline_jobs import projects


def test_bq_pipeline_integration(session_context, reseed_tables):
    """Test pipeline integration with bigquery."""
    dataset = projects.init_project_db.fn(project_id=-1)
    client = bigquery.Client()
    assert client.get_dataset(dataset)
