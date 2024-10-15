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


@router.patch(
    "/projects/{project_id}/classifiers/keyword_match/{classifier_id}/intermediatory_classes/{class_id}",
)
def patch_keyword_match_intemediatory_classes(
    session: deps.SessionDep,
    project_id: int,
    classifier_id: int,
    class_id: int,
    class_patch: base_schemas.IntermediatoryClassPatch,
) -> base_schemas.IntermediatoryClassResponse:
    """Patch the classes of a keyword match classifier."""
    return crud.patch_intermediatory_class(
        session=session,
        project_id=project_id,
        classifier_id=classifier_id,
        class_id=class_id,
        class_patch=class_patch,
    )


@router.delete(
    "/projects/{project_id}/classifiers/keyword_match/{classifier_id}/intermediatory_classes/{class_id}",
)
def delete_keyword_match_intemediatory_classes(
    session: deps.SessionDep,
    project_id: int,
    classifier_id: int,
    class_id: int,
) -> None:
    """Delete the classes of a keyword match classifier."""
    return crud.delete_intermediatory_class(
        session=session,
        project_id=project_id,
        classifier_id=classifier_id,
        class_id=class_id,
    )
