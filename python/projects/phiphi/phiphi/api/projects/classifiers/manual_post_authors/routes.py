"""Manual post authors routes."""
import fastapi

from phiphi.api import deps
from phiphi.api.projects import classifiers
from phiphi.api.projects.classifiers import base_schemas, response_schemas

router = fastapi.APIRouter()


@router.post(
    "/projects/{project_id}/classifiers/manual_post_authors",
)
def create_manual_post_authors_classifier(
    session: deps.SessionDep,
    project_id: int,
    classifier_create: base_schemas.ClassifierCreate,
) -> response_schemas.ClassifierDetail:
    """Create a new keyword match classifier."""
    return classifiers.crud.create_classifier(
        session=session,
        project_id=project_id,
        classifier_type=base_schemas.ClassifierType.manual_post_authors,
        classifier_create=classifier_create,
    )
