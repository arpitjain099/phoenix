"""Routes for gathers."""
import fastapi

from phiphi.api import deps
from phiphi.api.projects.gathers import child_crud, child_routes, child_types, crud, schemas

router = fastapi.APIRouter()
router.include_router(child_routes.router)


@router.get(
    "/projects/{project_id}/gathers/",
    response_model=list[schemas.GatherResponse],
    response_model_by_alias=False,
)
def get_gathers(
    session: deps.SessionDep, project_id: int, start: int = 0, end: int = 100
) -> list[schemas.GatherResponse]:
    """Get gathers."""
    return crud.get_gathers(session, project_id, start, end)


@router.get(
    "/projects/{project_id}/gathers/{gather_id}",
    response_model=child_types.AllChildTypesUnion,
    response_model_by_alias=False,
)
def get_gather(
    project_id: int, gather_id: int, session: deps.SessionDep
) -> child_types.AllChildTypesUnion:
    """Get an apify gather."""
    gather = child_crud.get_child_gather(session, project_id, gather_id)
    if gather is None:
        raise fastapi.HTTPException(status_code=404, detail="Gather not found")
    return gather


@router.get(
    "/projects/{project_id}/gathers/{gather_id}/estimate",
    response_model=schemas.GatherEstimate,
    response_model_by_alias=False,
)
def get_gather_estimate(
    project_id: int, gather_id: int, session: deps.SessionDep
) -> schemas.GatherEstimate:
    """Get an gather estimate.

    This is a dummy function that returns a dummy estimate.
    """
    return schemas.GatherEstimate(
        id=gather_id,
        # Setting this to 0 to indicate that the estimate is not available.
        estimated_credit_cost=0,
        estimated_duration_minutes=0,
    )


@router.delete(
    "/projects/{project_id}/gathers/{gather_id}",
    response_model=schemas.GatherResponse,
    response_model_by_alias=False,
)
async def delete_gather(
    project_id: int, gather_id: int, session: deps.SessionDep
) -> schemas.GatherResponse:
    """Delete a gather."""
    gather_response = await crud.delete(session, project_id, gather_id)
    return gather_response
