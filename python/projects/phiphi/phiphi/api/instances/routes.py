"""Routes for the instances."""
import fastapi
from phiphi.api import deps
from phiphi.api.instances import crud, schemas

router = fastapi.APIRouter()


@router.post("/instances/", response_model=schemas.Instance)
def create_instance(
    instance: schemas.InstanceCreate, session: deps.SessionDep
) -> schemas.Instance:
    """Create a new instance."""
    return crud.create_instance(session, instance)
