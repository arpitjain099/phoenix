"""Routes for gathers."""
import fastapi
from phiphi.api import deps, exceptions
from phiphi.api.instances.instance_runs import crud, schemas

router = fastapi.APIRouter()


@router.post("/instances/{instance_id}/runs/", response_model=schemas.InstanceRunsResponse)
def create_instance_runs(
    instance_id: int,
    session: deps.SessionDep,
) -> schemas.InstanceRunsResponse:
    """Create a new instance run."""
    try:
        return crud.create_instance_runs(session, instance_id)
    except exceptions.InstanceNotFound:
        raise exceptions.InstanceNotFound


@router.get("/instances/{instance_id}/runs/", response_model=list[schemas.InstanceRunsResponse])
def get_instance_runs(
    session: deps.SessionDep,
    instance_id: int,
    start: int = 0,
    end: int = 100,
) -> list[schemas.InstanceRunsResponse]:
    """Get instance runs."""
    try:
        return crud.get_instance_runs(session, instance_id, start, end)
    except exceptions.InstanceNotFound:
        raise exceptions.InstanceNotFound


@router.get(
    "/instances/{instance_id}/runs/filter/", response_model=list[schemas.InstanceRunsResponse]
)
def get_instance_runs_filter_by_run_statu(
    session: deps.SessionDep,
    instance_id: int,
    run_status: schemas.RunStatus,
    start: int = 0,
    end: int = 100,
) -> list[schemas.InstanceRunsResponse]:
    """Get instance runs."""
    try:
        return crud.get_instance_runs_by_run_status_filter(
            session, instance_id, run_status, start, end
        )
    except exceptions.InstanceNotFound:
        raise exceptions.InstanceNotFound


@router.get(
    "/instances/{instance_id}/runs/last/",
    response_model=schemas.InstanceRunsResponse,
)
def get_instance_last_run(
    instance_id: int, session: deps.SessionDep
) -> schemas.InstanceRunsResponse:
    """Get last instance run."""
    try:
        instance_runs = crud.get_instance_last_run(session, instance_id)
        if instance_runs is None:
            raise fastapi.HTTPException(status_code=404, detail="Instance has no previous runs")
        return instance_runs
    except exceptions.InstanceNotFound:
        raise exceptions.InstanceNotFound


@router.put("/instances/runs/{instance_runs_id}/", response_model=schemas.InstanceRunsResponse)
def update_instance(
    instance_runs_id: int, instance_runs: schemas.InstanceRunsUpdate, session: deps.SessionDep
) -> schemas.InstanceRunsResponse:
    """Update an instance run."""
    updated_instance = crud.update_instance_runs(session, instance_runs_id, instance_runs)
    if updated_instance is None:
        raise fastapi.HTTPException(status_code=404, detail="Instance runs not found")
    return updated_instance
