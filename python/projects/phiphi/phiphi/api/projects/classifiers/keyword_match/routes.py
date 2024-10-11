"""Keyword Match routes."""
import fastapi

from phiphi.api import deps
from phiphi.api.projects.classifiers import base_schemas, response_schemas
from phiphi.api.projects.classifiers import crud_v2 as crud

router = fastapi.APIRouter()


@router.post(
    "/projects/{project_id}/classifiers/keyword_match",
)
def create_keyword_match_classifier(
    session: deps.SessionDep,
    project_id: int,
    classifier_create: base_schemas.ClassifierCreate,
) -> response_schemas.Classifier:
    """Create a new keyword match classifier."""
    return crud.create_classifier(
        session=session,
        project_id=project_id,
        classifier_type=base_schemas.ClassifierType.keyword_match,
        classifier_create=classifier_create,
    )
