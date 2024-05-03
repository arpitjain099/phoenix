"""Routes for gathers."""
import fastapi
from phiphi.api import deps
from phiphi.api.projects.gathers import crud, schemas
from phiphi.api.projects.gathers.apify_facebook_posts import routes as apify_facebook_posts_routes

router = fastapi.APIRouter()
router.include_router(apify_facebook_posts_routes.router)


# REFACTORABLE: IF there are other gather subclasses, this should be refactored
# to support polymorphic models and multiple return types
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
