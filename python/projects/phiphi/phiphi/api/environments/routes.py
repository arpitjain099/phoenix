"""Routes for the environments."""
import fastapi
from phiphi.api import deps
from phiphi.api.environments import crud, schemas

router = fastapi.APIRouter()


@router.post("/environments/", response_model=schemas.EnvironmentResponse)
def create_environment(
    environment: schemas.EnvironmentCreate, session: deps.SessionDep
) -> schemas.EnvironmentResponse:
    """Create a new environment."""
    try:
        return crud.create_environment(session, environment)
    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e))


@router.put("/environments/{environment_id}", response_model=schemas.EnvironmentResponse)
def update_environment(
    environment_id: int, environment: schemas.EnvironmentUpdate, session: deps.SessionDep
) -> schemas.EnvironmentResponse:
    """Update an environment."""
    updated_environment = crud.update_environment(session, environment_id, environment)
    if updated_environment is None:
        raise fastapi.HTTPException(status_code=404, detail="Environment not found")
    return updated_environment


@router.get("/environments/{slug}", response_model=schemas.EnvironmentResponse)
def get_environment(slug: str, session: deps.SessionDep) -> schemas.EnvironmentResponse:
    """Get an environment."""
    environment = crud.get_environment(session, slug)
    if environment is None:
        raise fastapi.HTTPException(status_code=404, detail="Environment not found")
    return environment


@router.get("/environments/", response_model=list[schemas.EnvironmentResponse])
def get_environments(
    session: deps.SessionDep, start: int = 0, end: int = 100
) -> list[schemas.EnvironmentResponse]:
    """Get Environments."""
    return crud.get_environments(session, start, end)


@router.get("/environments/slug/", response_model=schemas.SlugResponse)
def get_unique_slug(environment_name: str, session: deps.SessionDep) -> schemas.SlugResponse:
    """Get unique slug."""
    try:
        return crud.get_unique_slug(session, environment_name)
    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e))
