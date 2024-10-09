"""Keyword Match routes."""
import fastapi

from phiphi.api import deps
from phiphi.api.projects.classifiers import base_schemas, child_crud
from phiphi.api.projects.classifiers.keyword_match import schemas as keyword_match_schemas

router = fastapi.APIRouter()


@router.post(
    "/projects/{project_id}/classifiers/keyword_match",
)
def create_keyword_match_classifier(
    session: deps.SessionDep,
    project_id: int,
    classifier_create: keyword_match_schemas.KeywordMatchClassifierCreate,
) -> None:
    """Create a new keyword match classifier."""
    child_crud.create_classifier(
        session=session,
        project_id=project_id,
        classifier_type=base_schemas.ClassifierType.keyword_match,
        classifier_create=classifier_create,
    )
    return None
