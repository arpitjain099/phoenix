"""Routes for the instances."""
import fastapi

from phiphi.api import deps, exceptions
from phiphi.api.instances import crud, schemas

router = fastapi.APIRouter()


@router.post("/instances/", response_model=schemas.InstanceResponse)
def create_instance(
    instance: schemas.InstanceCreate, session: deps.SessionDep
) -> schemas.InstanceResponse:
    """Create a new instance."""
    try:
        return crud.create_instance(session, instance)
    except exceptions.EnvironmentNotFound:
        raise exceptions.EnvironmentNotFound


@router.put("/instances/{instance_id}", response_model=schemas.InstanceResponse)
def update_instance(
    instance_id: int, instance: schemas.InstanceUpdate, session: deps.SessionDep
) -> schemas.InstanceResponse:
    """Update an instance."""
    updated_instance = crud.update_instance(session, instance_id, instance)
    if updated_instance is None:
        raise fastapi.HTTPException(status_code=404, detail="Instance not found")
    return updated_instance


@router.get("/instances/{instance_id}", response_model=schemas.InstanceResponse)
def get_instance(instance_id: int, session: deps.SessionDep) -> schemas.InstanceResponse:
    """Get an Instance."""
    instance = crud.get_instance(session, instance_id)
    if instance is None:
        raise fastapi.HTTPException(status_code=404, detail="Instance not found")
    return instance


@router.get("/instances/", response_model=list[schemas.InstanceResponse])
def get_instances(
    session: deps.SessionDep, start: int = 0, end: int = 100
) -> list[schemas.InstanceResponse]:
    """Get Instances."""
    return crud.get_instances(session, start, end)
