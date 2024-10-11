"""Classifier routes."""
import fastapi

from phiphi.api import deps, exceptions
from phiphi.api.projects.classifiers import crud_v2 as crud
from phiphi.api.projects.classifiers import response_schemas
from phiphi.api.projects.classifiers.keyword_match import routes as keyword_match_routes

router = fastapi.APIRouter()
router.include_router(keyword_match_routes.router)


@router.get(
    "/projects/{project_id}/classifiers/{classifier_id}",
)
def get_classifier(
    session: deps.SessionDep,
    project_id: int,
    classifier_id: int,
) -> response_schemas.Classifier:
    """Get a classifier."""
    classifier = crud.get_classifier(
        session=session, project_id=project_id, classifier_id=classifier_id
    )
    if classifier is None:
        raise exceptions.ClassifierNotFound()
    return classifier


@router.get(
    "/projects/{project_id}/classifiers",
    response_model=list[response_schemas.ClassifierList],
)
def get_classifiers(
    session: deps.SessionDep,
    project_id: int,
    start: int = 0,
    end: int = 100,
) -> list[response_schemas.ClassifierList]:
    """Get classifiers."""
    return crud.get_classifiers(session=session, project_id=project_id, start=start, end=end)
