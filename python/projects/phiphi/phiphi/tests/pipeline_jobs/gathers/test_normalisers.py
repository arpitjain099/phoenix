"""Tests for normalisers."""
from datetime import datetime

import pandas as pd
import pytest

from phiphi.api.projects.gathers import schemas
from phiphi.pipeline_jobs.gathers import normalise, normalisers, utils


@pytest.mark.freeze_time("2024-04-02T12:10:59.000Z")
def test_normaliser_facebook_posts(normalised_facebook_posts_df, facebook_posts_gather_fixture):
    """Test normaliser for facebook posts function.

    Note: we use the `normalise_batch` function from the `normalise` module to test the normaliser,
    as this is an easy way to test multiple records (and tests in the usage context).
    """
    batch_json = utils.load_sample_raw_data(
        source=schemas.Source.apify,
        platform=schemas.Platform.facebook,
        data_type=schemas.DataType.posts,
    )

    processed_df = normalise.normalise_batch(
        normaliser=normalisers.normalise_single_facebook_posts_json,
        batch_json=batch_json,
        gather=facebook_posts_gather_fixture,
        gather_batch_id=3,
        gathered_at=datetime.fromisoformat("2024-04-01T12:00:00.000Z"),
    )

    pd.testing.assert_frame_equal(processed_df, normalised_facebook_posts_df)


@pytest.mark.freeze_time("2024-04-02T12:10:59.000Z")
def test_normaliser_facebook_comments(
    normalised_facebook_comments_df, facebook_comments_gather_fixture
):
    """Test normaliser for facebook posts function.

    Note: we use the `normalise_batch` function from the `normalise` module to test the normaliser,
    as this is an easy way to test multiple records (and tests in the usage context).
    """
    batch_json = utils.load_sample_raw_data(
        source=schemas.Source.apify,
        platform=schemas.Platform.facebook,
        data_type=schemas.DataType.comments,
    )

    processed_df = normalise.normalise_batch(
        normaliser=normalisers.normalise_single_facebook_comments_json,
        batch_json=batch_json,
        gather=facebook_comments_gather_fixture,
        gather_batch_id=3,
        gathered_at=datetime.fromisoformat("2024-04-01T12:00:00.000Z"),
    )

    pd.testing.assert_frame_equal(processed_df, normalised_facebook_comments_df)
