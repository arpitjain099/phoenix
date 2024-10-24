"""Manual post authors routes."""
import fastapi

from phiphi.api import deps
from phiphi.api.projects import classifiers
from phiphi.api.projects.classifiers import base_schemas, response_schemas
from phiphi.api.projects.classifiers.manual_post_authors import crud, schemas

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


@router.post(
    "/projects/{project_id}/classifiers/manual_post_authors/{classifier_id}/intermediatory_classified_post_authors",
)
def create_intermediatory_classified_post_author(
    session: deps.SessionDep,
    project_id: int,
    classifier_id: int,
    create_obj: schemas.IntermediatoryClassifiedPostAuthorsCreate,
) -> schemas.IntermediatoryClassifiedPostAuthorsResponse:
    """Create an intermediatory classified post author."""
    return crud.create_intermediatory_classified_post_authors(
        session=session,
        project_id=project_id,
        classifier_id=classifier_id,
        create_obj=create_obj,
    )


@router.delete(
    "/projects/{project_id}/classifiers/manual_post_authors/{classifier_id}/intermediatory_classified_post_authors/{classified_post_author_id}",
)
def delete_intermediatory_classified_post_author(
    session: deps.SessionDep,
    project_id: int,
    classifier_id: int,
    classified_post_author_id: int,
) -> None:
    """Delete an intermediatory classified post author."""
    return crud.delete_intermediatory_classified_post_author(
        session=session,
        project_id=project_id,
        classifier_id=classifier_id,
        classified_post_author_id=classified_post_author_id,
    )
