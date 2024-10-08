"""Test gather_classify_tabulate_flow.py."""
from unittest import mock

import pytest

from phiphi.pipeline_jobs.composite_flows import gather_classify_tabulate_flow
from phiphi.tests.pipeline_jobs.gathers import example_gathers

PATCH_SETTINGS = {
    "USE_MOCK_APIFY": True,
    # We are not using the mock Big Query as we are going to use a mock patch
    "USE_MOCK_BQ": False,
    "APIFY_API_KEYS": {"main": "dummy_key"},
}


@mock.patch("phiphi.pipeline_jobs.gathers.apify_scrape.apify_scrape_and_batch_download_results")
@mock.patch("phiphi.pipeline_jobs.classify.flow.classify_flow")
@mock.patch("google.cloud.bigquery.Client")
@mock.patch("pandas.read_gbq")
@pytest.mark.patch_settings(PATCH_SETTINGS)
@pytest.mark.asyncio
async def test_gather_classify_tabulate_flow(
    mock_read_gbq,
    mock_bigquery_client,
    mock_classify_flow,
    mock_apify_scrape_and_batch_download_results,
    patch_settings,
    prefect_test_fixture,
):
    """Test gather_classify_tabulate_flow runs correctly."""
    gather = example_gathers.facebook_comments_gather_example()
    # Due to prefect doing some magic with flows that return None we are not testing the return
    # value.
    await gather_classify_tabulate_flow.gather_classify_tabulate_flow(
        project_id=5,
        job_source_id=5,
        job_run_id=5,
        project_namespace="project_id5",
        gather_dict=gather.model_dump(),
        gather_child_type=gather.child_type,
        classifiers_dict_list=[],
        active_classifiers_versions=[],
        batch_size=1,
    )
    mock_apify_scrape_and_batch_download_results.assert_called_once()
    assert mock_bigquery_client.call_count == 2
    mock_read_gbq.assert_called_once()
    mock_classify_flow.assert_not_called()


@mock.patch("phiphi.pipeline_jobs.gathers.apify_scrape.apify_scrape_and_batch_download_results")
@mock.patch("phiphi.pipeline_jobs.classify.flow.classify_flow")
@mock.patch("google.cloud.bigquery.Client")
@mock.patch("pandas.read_gbq")
@pytest.mark.patch_settings(PATCH_SETTINGS)
@pytest.mark.asyncio
async def test_gather_classify_tabulate_flow_exception_propagate(
    mock_read_gbq,
    mock_bigquery_client,
    mock_classify_flow,
    mock_apify_scrape_and_batch_download_results,
    patch_settings,
    prefect_test_fixture,
):
    """Test subflow exceptions are propagated in gather_classify_tabulate_flow."""
    gather = example_gathers.facebook_comments_gather_example()
    mock_read_gbq.side_effect = Exception("Test")
    with pytest.raises(Exception):
        await gather_classify_tabulate_flow.gather_classify_tabulate_flow(
            project_id=5,
            job_source_id=5,
            job_run_id=5,
            project_namespace="project_id5",
            gather_dict=gather.model_dump(),
            gather_child_type=gather.child_type,
            classifiers_dict_list=[],
            active_classifiers_versions=[],
            batch_size=1,
        )
        mock_apify_scrape_and_batch_download_results.assert_called_once()
        mock_bigquery_client.assert_not_called()
        mock_classify_flow.assert_not_called()


@mock.patch("phiphi.pipeline_jobs.gathers.apify_scrape.apify_scrape_and_batch_download_results")
@mock.patch("phiphi.pipeline_jobs.classify.flow.classify_flow")
@mock.patch("google.cloud.bigquery.Client")
@mock.patch("pandas.read_gbq")
@pytest.mark.patch_settings(PATCH_SETTINGS)
@pytest.mark.asyncio
async def test_gather_classify_tabulate_flow_with_classify(
    mock_read_gbq,
    mock_bigquery_client,
    mock_classify_flow,
    mock_apify_scrape_and_batch_download_results,
    patch_settings,
    prefect_test_fixture,
):
    """Test gather_classify_tabulate_flow."""
    gather = example_gathers.facebook_comments_gather_example()
    classify_dict = {"check": "check"}
    active_classifiers_versions = [(1, 1)]
    # Due to prefect doing some magic with flows that return None we are not testing the return
    # value.
    await gather_classify_tabulate_flow.gather_classify_tabulate_flow(
        project_id=5,
        job_source_id=5,
        job_run_id=5,
        project_namespace="project_id5",
        gather_dict=gather.model_dump(),
        gather_child_type=gather.child_type,
        classifiers_dict_list=[classify_dict, classify_dict],
        active_classifiers_versions=active_classifiers_versions,
        batch_size=1,
    )
    mock_apify_scrape_and_batch_download_results.assert_called_once()
    assert mock_classify_flow.call_count == 2
    assert mock_bigquery_client.call_count == 2
    mock_read_gbq.assert_called_once()


@mock.patch("phiphi.pipeline_jobs.gathers.apify_scrape.apify_scrape_and_batch_download_results")
@mock.patch("phiphi.pipeline_jobs.classify.flow.classify_flow")
@mock.patch("google.cloud.bigquery.Client")
@mock.patch("pandas.read_gbq")
@pytest.mark.patch_settings(PATCH_SETTINGS)
@pytest.mark.asyncio
async def test_gather_classify_tabulate_flow_with_classify_exception(
    mock_read_gbq,
    mock_bigquery_client,
    mock_classify_flow,
    mock_apify_scrape_and_batch_download_results,
    patch_settings,
    prefect_test_fixture,
):
    """Test gather_classify_tabulate_flow.

    Currently we do not raise the exception from classify_flow.
    """
    gather = example_gathers.facebook_comments_gather_example()
    classify_dict = {"check": "check"}
    active_classifiers_versions = [(1, 1)]
    mock_classify_flow.side_effect = Exception("Test")
    # Due to prefect doing some magic with flows that return None we are not testing the return
    # value.
    await gather_classify_tabulate_flow.gather_classify_tabulate_flow(
        project_id=5,
        job_source_id=5,
        job_run_id=5,
        project_namespace="project_id5",
        gather_dict=gather.model_dump(),
        gather_child_type=gather.child_type,
        classifiers_dict_list=[classify_dict, classify_dict],
        active_classifiers_versions=active_classifiers_versions,
        batch_size=1,
    )
    mock_apify_scrape_and_batch_download_results.assert_called_once()
    assert mock_classify_flow.call_count == 2
    assert mock_bigquery_client.call_count == 2
    mock_read_gbq.assert_called_once()
