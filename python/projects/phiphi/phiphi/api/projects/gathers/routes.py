"""Routes for gathers."""
import fastapi
from phiphi.api import deps
from phiphi.api.projects.gathers import child_routes, crud, schemas

router = fastapi.APIRouter()
router.include_router(child_routes.router)


@router.get("/projects/{project_id}/gathers/", response_model=list[schemas.GatherResponse])
def get_gathers(
    session: deps.SessionDep, project_id: int, start: int = 0, end: int = 100
) -> list[schemas.GatherResponse]:
    """Get gathers."""
    return crud.get_gathers(session, project_id, start, end)


@router.get(
    "/projects/{project_id}/gathers/{gather_id}",
    response_model=schemas.GatherResponse,
)
def get_gather(
    project_id: int, gather_id: int, session: deps.SessionDep
) -> schemas.GatherResponse:
    """Get an apify gather."""
    gather = crud.get_gather(session, project_id, gather_id)
    if gather is None:
        raise fastapi.HTTPException(status_code=404, detail="Gather not found")
    return gather


@router.get(
    "/projects/{project_id}/gathers/{gather_id}/estimate",
    response_model=schemas.GatherEstimate,
)
def get_gather_estimate(
    project_id: int, gather_id: int, session: deps.SessionDep
) -> schemas.GatherEstimate:
    """Get an gather estimate.

    This is a dummy function that returns a dummy estimate.
    """
    return schemas.GatherEstimate(
        id=gather_id,
        estimated_credit_cost=100,
        estimated_duration_minutes=30,
    )
