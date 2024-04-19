"""Routes for gathers."""
import fastapi
from phiphi.api import deps, exceptions
from phiphi.api.projects.gathers import crud, schemas

router = fastapi.APIRouter()


@router.post("/projects/{project_id}/gathers/apify", response_model=schemas.ApifyGatherResponse)
def create_apify_gather(
    gather: schemas.ApifyGatherCreate,
    project_id: int,
    session: deps.SessionDep,
) -> schemas.ApifyGatherResponse:
    """Create a new gather."""
    try:
        return crud.create_apify_gather(session, project_id, gather)
    except exceptions.ProjectNotFound:
        raise exceptions.ProjectNotFound


# REFACTORABLE: IF there are other gather subclasses, this should be refactored
# to support polymorphic models and multiple return types
@router.get("/projects/{project_id}/gathers/", response_model=list[schemas.ApifyGatherResponse])
def get_gathers(
    session: deps.SessionDep, project_id: int, start: int = 0, end: int = 100
) -> list[schemas.ApifyGatherResponse]:
    """Get gathers."""
    try:
        return crud.get_gathers(session, project_id, start, end)
    except exceptions.ProjectNotFound:
        raise exceptions.ProjectNotFound


@router.get(
    "/projects/{project_id}/gathers/apify/{apify_gather_id}",
    response_model=schemas.ApifyGatherResponse,
)
def get_apify_gather(
    project_id: int, apify_gather_id: int, session: deps.SessionDep
) -> schemas.ApifyGatherResponse:
    """Get an apify gather."""
    try:
        apify_gather = crud.get_apify_gather(session, project_id, apify_gather_id)
        if apify_gather is None:
            raise fastapi.HTTPException(status_code=404, detail="Gather not found")
        return apify_gather
    except exceptions.ProjectNotFound:
        raise exceptions.ProjectNotFound


@router.get(
    "/projects/{project_id}/gathers/apify", response_model=list[schemas.ApifyGatherResponse]
)
def get_apify_gathers(
    session: deps.SessionDep, project_id: int, start: int = 0, end: int = 100
) -> list[schemas.ApifyGatherResponse]:
    """Get apify gathers."""
    try:
        return crud.get_apify_gathers(session, project_id, start, end)
    except exceptions.ProjectNotFound:
        raise exceptions.ProjectNotFound
