"""Routes for gathers."""
import fastapi
from phiphi.api import deps
from phiphi.api.gathers import schemas

router = fastapi.APIRouter()


@router.post("/gathers/", response_model=schemas.Gather)
def create_gather(instance: schemas.GatherCreate, session: deps.SessionDep) -> schemas.Gather:
    """Create a new gather."""
    pass


@router.put("/gathers/{gather_id}", response_model=schemas.Gather)
def update_gather(
    gather_id: int, gather: schemas.GatherUpdate, session: deps.SessionDep
) -> schemas.Gather:
    """Update a gather."""
    pass


@router.get("/gathers/{gather_id}", response_model=schemas.Gather)
def get_instance(gather_id: int, session: deps.SessionDep) -> schemas.Gather:
    """Get a gather."""
    pass


@router.get("/gathers/", response_model=list[schemas.Gather])
def get_gathers(session: deps.SessionDep, start: int = 0, end: int = 100) -> list[schemas.Gather]:
    """Get gathers."""
    pass
