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
        child_type_name=schemas.ChildTypeName.apify_facebook_posts
    )

    processed_df = normalise.normalise_batch(
        normaliser=normalisers.normalise_single_facebook_posts_json,
        batch_json=batch_json,
        gather_id=facebook_posts_gather_fixture.id,
        gather_child_type=facebook_posts_gather_fixture.child_type,
        gather_batch_id=3,
        gathered_at=datetime.fromisoformat("2024-04-01T12:00:00.000Z"),
    )
    assert processed_df is not None
    pd.testing.assert_frame_equal(processed_df, normalised_facebook_posts_df)


@pytest.mark.freeze_time("2024-04-02T12:10:59.000Z")
def test_normaliser_facebook_search_posts(
    normalised_facebook_search_posts_df, facebook_search_posts_gather_fixture
):
    """Test normaliser for facebook posts function.

    Note: we use the `normalise_batch` function from the `normalise` module to test the normaliser,
    as this is an easy way to test multiple records (and tests in the usage context).
    """
    batch_json = utils.load_sample_raw_data(
        child_type_name=schemas.ChildTypeName.apify_facebook_search_posts
    )

    processed_df = normalise.normalise_batch(
        normaliser=normalisers.normalise_single_facebook_search_posts_json,
        batch_json=batch_json,
        gather_id=facebook_search_posts_gather_fixture.id,
        gather_child_type=facebook_search_posts_gather_fixture.child_type,
        gather_batch_id=3,
        gathered_at=datetime.fromisoformat("2024-04-01T12:00:00.000Z"),
    )
    assert processed_df is not None
    pd.testing.assert_frame_equal(processed_df, normalised_facebook_search_posts_df)


@pytest.mark.freeze_time("2024-04-02T12:10:59.000Z")
def test_normaliser_facebook_comments(
    normalised_facebook_comments_df, facebook_comments_gather_fixture
):
    """Test normaliser for facebook posts function.

    Note: we use the `normalise_batch` function from the `normalise` module to test the normaliser,
    as this is an easy way to test multiple records (and tests in the usage context).
    """
    batch_json = utils.load_sample_raw_data(
        child_type_name=schemas.ChildTypeName.apify_facebook_comments,
    )

    processed_df = normalise.normalise_batch(
        normaliser=normalisers.normalise_single_facebook_comments_json,
        batch_json=batch_json,
        gather_id=facebook_comments_gather_fixture.id,
        gather_child_type=facebook_comments_gather_fixture.child_type,
        gather_batch_id=3,
        gathered_at=datetime.fromisoformat("2024-04-01T12:00:00.000Z"),
    )
    assert processed_df is not None
    pd.testing.assert_frame_equal(processed_df, normalised_facebook_comments_df)


@pytest.mark.freeze_time("2024-04-02T12:10:59.000Z")
def test_normaliser_tiktok_accounts_posts(
    normalised_tiktok_accounts_posts_df, tiktok_accounts_posts_gather_fixture
):
    """Test normaliser for tiktok accounts posts function.

    Note: we use the `normalise_batch` function from the `normalise` module to test the normaliser,
    as this is an easy way to test multiple records (and tests in the usage context).
    """
    batch_json = utils.load_sample_raw_data(
        child_type_name=schemas.ChildTypeName.apify_tiktok_accounts_posts,
    )

    processed_df = normalise.normalise_batch(
        # all tiktok posts gathers are normalised the same way
        normaliser=normalisers.normalise_single_tiktok_posts_json,
        batch_json=batch_json,
        gather_id=tiktok_accounts_posts_gather_fixture.id,
        gather_child_type=tiktok_accounts_posts_gather_fixture.child_type,
        gather_batch_id=3,
        gathered_at=datetime.fromisoformat("2024-04-01T12:00:00.000Z"),
    )
    assert processed_df is not None
    pd.testing.assert_frame_equal(processed_df, normalised_tiktok_accounts_posts_df)


@pytest.mark.freeze_time("2024-04-02T12:10:59.000Z")
def test_normaliser_tiktok_hashtags_posts(
    normalised_tiktok_hashtags_posts_df, tiktok_hashtags_posts_gather_fixture
):
    """Test normaliser for tiktok hashtags posts function.

    Note: we use the `normalise_batch` function from the `normalise` module to test the normaliser,
    as this is an easy way to test multiple records (and tests in the usage context).
    """
    batch_json = utils.load_sample_raw_data(
        child_type_name=schemas.ChildTypeName.apify_tiktok_hashtags_posts,
    )

    processed_df = normalise.normalise_batch(
        # all tiktok posts gathers are normalised the same way
        normaliser=normalisers.normalise_single_tiktok_posts_json,
        batch_json=batch_json,
        gather_id=tiktok_hashtags_posts_gather_fixture.id,
        gather_child_type=tiktok_hashtags_posts_gather_fixture.child_type,
        gather_batch_id=3,
        gathered_at=datetime.fromisoformat("2024-04-01T12:00:00.000Z"),
    )
    assert processed_df is not None
    pd.testing.assert_frame_equal(processed_df, normalised_tiktok_hashtags_posts_df)


@pytest.mark.freeze_time("2024-04-02T12:10:59.000Z")
def test_normaliser_tiktok_searches_posts(
    normalised_tiktok_searches_posts_df, tiktok_searches_posts_gather_fixture
):
    """Test normaliser for tiktok searches posts function.

    Note: we use the `normalise_batch` function from the `normalise` module to test the normaliser,
    as this is an easy way to test multiple records (and tests in the usage context).
    """
    batch_json = utils.load_sample_raw_data(
        child_type_name=schemas.ChildTypeName.apify_tiktok_searches_posts,
    )

    processed_df = normalise.normalise_batch(
        # all tiktok posts gathers are normalised the same way
        normaliser=normalisers.normalise_single_tiktok_posts_json,
        batch_json=batch_json,
        gather_id=tiktok_searches_posts_gather_fixture.id,
        gather_child_type=tiktok_searches_posts_gather_fixture.child_type,
        gather_batch_id=3,
        gathered_at=datetime.fromisoformat("2024-04-01T12:00:00.000Z"),
    )
    assert processed_df is not None
    pd.testing.assert_frame_equal(processed_df, normalised_tiktok_searches_posts_df)


@pytest.mark.freeze_time("2024-04-02T12:10:59.000Z")
def test_normaliser_tiktok_comments(normalised_tiktok_comments_df, tiktok_comments_gather_fixture):
    """Test normaliser for tiktok comments function.

    Note: we use the `normalise_batch` function from the `normalise` module to test the normaliser,
    as this is an easy way to test multiple records (and tests in the usage context).
    """
    batch_json = utils.load_sample_raw_data(
        child_type_name=schemas.ChildTypeName.apify_tiktok_comments,
    )

    processed_df = normalise.normalise_batch(
        normaliser=normalisers.normalise_single_tiktok_comments_json,
        batch_json=batch_json,
        gather_id=tiktok_comments_gather_fixture.id,
        gather_child_type=tiktok_comments_gather_fixture.child_type,
        gather_batch_id=3,
        gathered_at=datetime.fromisoformat("2024-04-01T12:00:00.000Z"),
    )
    assert processed_df is not None
    pd.testing.assert_frame_equal(processed_df, normalised_tiktok_comments_df)
