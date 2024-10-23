"""Test generalised authors."""
import json

import pandas as pd
import pytest

from phiphi.pipeline_jobs import generalised_authors


@pytest.fixture
def sample_generalised_post_authors() -> pd.DataFrame:
    """Sample generalised post authors."""
    path = generalised_authors.get_generalised_post_author_sample_data_path()
    with open(path, "r") as f:
        sample_authors = json.load(f)

    return pd.DataFrame(sample_authors)


@pytest.mark.patch_settings({"USE_MOCK_BQ": True})
def test_get_post_authors_with_mock_bq(patch_settings, sample_generalised_post_authors):
    """Test get_post_authors when USE_MOCK_BQ is enabled."""
    result_df = generalised_authors.get_post_authors(
        project_namespace="test_project", offset=0, limit=2
    )
    pd.testing.assert_frame_equal(result_df, sample_generalised_post_authors[:2])
