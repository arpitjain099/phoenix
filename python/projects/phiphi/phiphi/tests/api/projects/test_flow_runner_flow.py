"""Test flow_runner_flow."""
from unittest import mock

from prefect.client.schemas import objects
from prefect.logging import disable_run_logger

from phiphi.api.projects.gathers import crud as gathers_crud
from phiphi.api.projects.job_runs import crud, flow_runner_flow, schemas


@mock.patch("phiphi.api.projects.job_runs.flow_runner_flow.wait_for_job_flow_run")
@mock.patch("phiphi.api.projects.job_runs.flow_runner_flow.start_flow_run")
def test_flow_runner_flow(
    mock_start_flow_run, mock_wait_for_flow_run, session_context, reseed_tables
):
    """Test the flow_runner_flow."""
    project_id = 1
    gather_id = 2
    job_run_create = schemas.JobRunCreate(
        foreign_id=gather_id, foreign_job_type=schemas.ForeignJobType.gather
    )

    job_run = crud.create_job_run(
        db=session_context, project_id=project_id, job_run_create=job_run_create
    )

    gather = gathers_crud.get_gather(
        session=session_context, project_id=project_id, gather_id=gather_id
    )

    mock_start_flow_state = mock.MagicMock()
    mock_start_flow_state.is_completed.return_value = True

    mock_wait_flow_state = mock.MagicMock()
    mock_wait_flow_state.is_completed.return_value = True

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
        flow_runner_flow.flow_runner_flow.fn(
            project_id=project_id,
            job_type=job_run.foreign_job_type.value,
            job_source_id=job_run.foreign_id,
            job_run_id=job_run.id,
        )

    mock_start_flow_run.assert_called_once_with(
        project_id=project_id,
        job_type=job_run.foreign_job_type,
        job_source_id=job_run.foreign_id,
        job_run_id=job_run.id,
        job_params=gather,
    )
    mock_wait_for_flow_run.assert_called_once_with(job_run_flow=mock_return_start_flow_run)

    job_run_completed = crud.get_job_run(
        db=session_context, project_id=project_id, job_run_id=job_run.id
    )

    assert job_run_completed
    assert job_run_completed.id == job_run.id
    assert job_run_completed.status == schemas.Status.completed_sucessfully
    assert job_run_completed.completed_at is not None
