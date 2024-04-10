"""Routes for gathers."""
import fastapi
from phiphi.api import deps
from phiphi.api.gathers import crud, schemas

router = fastapi.APIRouter()


@router.post("/gathers/apify", response_model=schemas.ApifyGatherResponse)
def create_apify_gather(
    gather: schemas.ApifyGatherCreate, session: deps.SessionDep
) -> schemas.ApifyGatherResponse:
    """Create a new gather."""
    return crud.create_apify_gather(session, gather)


# REFACTORABLE: IF there are other gather subclasses, this should be refactored
# to support polymorphic models and multiple return types
@router.get("/gathers/", response_model=schemas.ApifyGatherResponse)
def get_gathers(
    session: deps.SessionDep, start: int = 0, end: int = 100
) -> list[schemas.ApifyGatherResponse]:
    """Get gathers."""
    return crud.get_gathers(session, start, end)


@router.get("/gathers/apify/{apify_gather_id}", response_model=schemas.ApifyGatherResponse)
def get_apify_gather(
    apify_gather_id: int, session: deps.SessionDep, start: int = 0, end: int = 100
) -> schemas.ApifyGatherResponse:
    """Get an apify gather."""
    apify_gather = crud.get_apify_gather(session, apify_gather_id)
    if apify_gather is None:
        raise fastapi.HTTPException(status_code=404, detail="Gather not found")
    return apify_gather


@router.get("/gathers/apify", response_model=list[schemas.ApifyGatherResponse])
def get_apify_gathers(
    session: deps.SessionDep, start: int = 0, end: int = 100
) -> list[schemas.ApifyGatherResponse]:
    """Get apify gathers."""
    return crud.get_apify_gathers(session, start, end)
