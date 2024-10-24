"""Test generalised authors."""
import pandas as pd
import pytest

from phiphi.pipeline_jobs import generalised_authors


@pytest.mark.patch_settings({"USE_MOCK_BQ": True})
def test_get_post_authors_with_mock_bq(
    patch_settings, pipeline_jobs_sample_generalised_post_authors
):
    """Test get_post_authors when USE_MOCK_BQ is enabled."""
    result_df = generalised_authors.get_post_authors(
        project_namespace="test_project", offset=0, limit=2
    )
    expected_df = pipeline_jobs_sample_generalised_post_authors[:2]
    pd.testing.assert_frame_equal(result_df, expected_df)
