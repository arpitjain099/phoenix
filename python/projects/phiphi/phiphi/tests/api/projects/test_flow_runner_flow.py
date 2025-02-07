"""Test the flow_runner_flow."""
from unittest import mock
from unittest.mock import AsyncMock

import pytest
from prefect.client.schemas import objects
from prefect.logging import disable_run_logger

from phiphi.api.projects.job_runs import crud, flow_runner_flow, schemas


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "foreign_id,foreign_job_type,expected_deployment_name,mock_return_wait_flow_run_completed,expected_job_run_status",
    [
        (
            2,
            schemas.ForeignJobType.gather,
            "gather_flow/gather_flow",
            True,
            schemas.Status.completed_successfully,
        ),
        (
            2,
            schemas.ForeignJobType.gather,
            "gather_flow/gather_flow",
            False,
            schemas.Status.failed,
        ),
        (
            0,
            schemas.ForeignJobType.tabulate,
            "tabulate_flow/tabulate_flow",
            True,
            schemas.Status.completed_successfully,
        ),
        (
            2,
            schemas.ForeignJobType.delete_gather,
            "delete_gather_flow/delete_gather_flow",
            True,
            schemas.Status.completed_successfully,
        ),
    ],
)
@mock.patch("prefect.flow_runs.wait_for_flow_run", new_callable=AsyncMock)
@mock.patch("prefect.deployments.deployments.run_deployment", new_callable=AsyncMock)
async def test_flow_runner_flow(
    mock_start_flow_run,
    mock_wait_for_flow_run,
    foreign_id,
    foreign_job_type,
    expected_deployment_name,
    mock_return_wait_flow_run_completed,
    expected_job_run_status,
    session_context,
    reseed_tables,
):
    """Test the flow_runner_flow."""
    project_id = 1
    job_run_create = schemas.JobRunCreate(foreign_id=foreign_id, foreign_job_type=foreign_job_type)

    job_run = crud.create_job_run(
        session=session_context, project_id=project_id, job_run_create=job_run_create
    )

    mock_start_flow_state = mock.MagicMock()
    mock_start_flow_state.is_completed.return_value = True

    mock_wait_flow_state = mock.MagicMock()
    mock_wait_flow_state.is_completed.return_value = mock_return_wait_flow_run_completed

    assert job_run.status == schemas.Status.awaiting_start

    mock_return_start_flow_run = mock.MagicMock(spec=objects.FlowRun)
    mock_return_start_flow_run.id = "mock_uuid"
    mock_return_start_flow_run.name = "mock_start_flow_run"
    mock_return_start_flow_run.state = mock_start_flow_state
    mock_start_flow_run.return_value = mock_return_start_flow_run

    mock_return_wait_flow_run = mock.MagicMock(spec=objects.FlowRun)
    mock_return_wait_flow_run.id = "mock_uuid"
    mock_return_wait_flow_run.name = "mock_wait_flow_run"
    mock_return_wait_flow_run.state = mock_wait_flow_state
    mock_wait_for_flow_run.return_value = mock_return_wait_flow_run

    with disable_run_logger():
        await flow_runner_flow.flow_runner_flow.fn(
            project_id=project_id,
            job_type=job_run.foreign_job_type,
            job_source_id=job_run.foreign_id,
            job_run_id=job_run.id,
        )

    # with the async functions it is very hard to test the arguments
    # so we just test that the functions were called
    mock_start_flow_run.assert_called_once()
    args = mock_start_flow_run.call_args.kwargs
    assert "name" in args
    assert args["name"] == expected_deployment_name
    mock_wait_for_flow_run.assert_called_once_with(flow_run_id=mock_return_start_flow_run.id)

    job_run_completed = crud.get_job_run(
        session=session_context, project_id=project_id, job_run_id=job_run.id
    )

    assert job_run_completed
    assert job_run_completed.id == job_run.id
    assert job_run_completed.status == expected_job_run_status
    assert job_run_completed.completed_at is not None


@pytest.mark.asyncio
@mock.patch("phiphi.api.projects.job_runs.flow_runner_flow.start_flow_run", new_callable=AsyncMock)
async def test_flow_runner_flow_exception(mock_start_flow_run, session_context, reseed_tables):
    """Test the flow_runner_flow if there is an exception."""
    project_id = 1
    gather_id = 2
    job_run_create = schemas.JobRunCreate(
        foreign_id=gather_id, foreign_job_type=schemas.ForeignJobType.gather
    )

    job_run = crud.create_job_run(
        session=session_context, project_id=project_id, job_run_create=job_run_create
    )

    mock_start_flow_run.side_effect = Exception(
        "Mock (correctly) triggered exception, for testing."
    )

    assert job_run.status == schemas.Status.awaiting_start

    with pytest.raises(Exception):
        await flow_runner_flow.flow_runner_flow(
            project_id=project_id,
            job_type=job_run.foreign_job_type,
            job_source_id=job_run.foreign_id,
            job_run_id=job_run.id,
        )

    job_run_completed = crud.get_job_run(
        session=session_context, project_id=project_id, job_run_id=job_run.id
    )

    assert job_run_completed
    assert job_run_completed.id == job_run.id
    assert job_run_completed.status == schemas.Status.failed
    assert job_run_completed.completed_at is not None
