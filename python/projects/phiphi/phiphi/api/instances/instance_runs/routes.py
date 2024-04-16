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
    session: deps.SessionDep, instance_id: int, start: int = 0, end: int = 100
) -> list[schemas.InstanceRunsResponse]:
    """Get gathers."""
    try:
        return crud.get_instance_runs(session, instance_id, start, end)
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
            raise fastapi.HTTPException(status_code=404, detail="Instance run not found")
        return instance_runs
    except exceptions.InstanceNotFound:
        raise exceptions.InstanceNotFound
