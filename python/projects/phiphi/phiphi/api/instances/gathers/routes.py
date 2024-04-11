"""Routes for gathers."""
import fastapi
from phiphi.api import deps
from phiphi.api.instances.gathers import crud, schemas

router = fastapi.APIRouter()


@router.post("/instances/{instance_id}/gathers/apify", response_model=schemas.ApifyGatherResponse)
def create_apify_gather(
    gather: schemas.ApifyGatherCreate,
    instance_id: int,
    session: deps.SessionDep,
) -> schemas.ApifyGatherResponse:
    """Create a new gather."""
    return crud.create_apify_gather(session, instance_id, gather)


# REFACTORABLE: IF there are other gather subclasses, this should be refactored
# to support polymorphic models and multiple return types
@router.get("/instances/{instance_id}/gathers/", response_model=list[schemas.ApifyGatherResponse])
def get_gathers(
    session: deps.SessionDep, instance_id: int, start: int = 0, end: int = 100
) -> list[schemas.ApifyGatherResponse]:
    """Get gathers."""
    return crud.get_gathers(session, instance_id, start, end)


@router.get(
    "/instances/{instance_id}/gathers/apify/{apify_gather_id}",
    response_model=schemas.ApifyGatherResponse,
)
def get_apify_gather(
    instance_id: int, apify_gather_id: int, session: deps.SessionDep
) -> schemas.ApifyGatherResponse:
    """Get an apify gather."""
    apify_gather = crud.get_apify_gather(session, instance_id, apify_gather_id)
    if apify_gather is None:
        raise fastapi.HTTPException(status_code=404, detail="Gather not found")
    return apify_gather


@router.get(
    "/instances/{instance_id}/gathers/apify", response_model=list[schemas.ApifyGatherResponse]
)
def get_apify_gathers(
    session: deps.SessionDep, instance_id: int, start: int = 0, end: int = 100
) -> list[schemas.ApifyGatherResponse]:
    """Get apify gathers."""
    return crud.get_apify_gathers(session, instance_id, start, end)
