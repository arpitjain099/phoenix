"""Keyword Match routes."""
import fastapi

from phiphi.api import deps
from phiphi.api.projects.classifiers import base_schemas, response_schemas
from phiphi.api.projects.classifiers import crud_v2 as classifiers_crud
from phiphi.api.projects.classifiers.keyword_match import crud, schemas

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
    return classifiers_crud.create_classifier(
        session=session,
        project_id=project_id,
        classifier_type=base_schemas.ClassifierType.keyword_match,
        classifier_create=classifier_create,
    )


@router.post(
    "/projects/{project_id}/classifiers/keyword_match/{classifier_id}/version_and_run",
)
async def create_keyword_match_version_and_run(
    session: deps.SessionDep,
    project_id: int,
    classifier_id: int,
) -> response_schemas.Classifier:
    """Create a new keyword match version and run."""
    return await crud.create_version_and_run(
        session=session,
        project_id=project_id,
        classifier_id=classifier_id,
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
    return classifiers_crud.patch_intermediatory_class(
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
    return classifiers_crud.delete_intermediatory_class(
        session=session,
        project_id=project_id,
        classifier_id=classifier_id,
        class_id=class_id,
    )


@router.post(
    "/projects/{project_id}/classifiers/keyword_match/{classifier_id}/intermediatory_classes"
)
def create_keyword_match_intemediatory_classes(
    session: deps.SessionDep,
    project_id: int,
    classifier_id: int,
    class_create: base_schemas.IntermediatoryClassCreate,
) -> base_schemas.IntermediatoryClassResponse:
    """Create the classes of a keyword match classifier."""
    return classifiers_crud.create_intermediatory_class(
        session=session,
        project_id=project_id,
        classifier_id=classifier_id,
        class_create=class_create,
    )


@router.post(
    "/projects/{project_id}/classifiers/keyword_match/{classifier_id}/intermediatory_class_to_keyword_configs",
)
def create_keyword_match_intermediatory_class_to_keyword_config(
    session: deps.SessionDep,
    project_id: int,
    classifier_id: int,
    intermediatory_class_to_keyword_config: schemas.IntermediatoryClassToKeywordConfigCreate,
) -> schemas.IntermediatoryClassToKeywordConfigResponse:
    """Create an intermediatory class to keyword config."""
    return crud.create_intermediatory_class_to_keyword_config(
        session=session,
        project_id=project_id,
        classifier_id=classifier_id,
        intermediatory_class_to_keyword_config=intermediatory_class_to_keyword_config,
    )


@router.patch(
    "/projects/{project_id}/classifiers/keyword_match/{classifier_id}/intermediatory_class_to_keyword_configs/{config_id}",
)
def patch_keyword_match_intermediatory_class_to_keyword_config(
    session: deps.SessionDep,
    project_id: int,
    classifier_id: int,
    config_id: int,
    intermediatory_class_to_keyword_config: schemas.IntermediatoryClassToKeywordConfigPatch,
) -> schemas.IntermediatoryClassToKeywordConfigResponse:
    """Patch an intermediatory class to keyword config."""
    return crud.patch_intermediatory_class_to_keyword_config(
        session=session,
        project_id=project_id,
        classifier_id=classifier_id,
        intermediatory_class_to_keyword_config_id=config_id,
        intermediatory_class_to_keyword_config=intermediatory_class_to_keyword_config,
    )


@router.delete(
    "/projects/{project_id}/classifiers/keyword_match/{classifier_id}/intermediatory_class_to_keyword_configs/{config_id}",
)
def delete_keyword_match_intermediatory_class_to_keyword_config(
    session: deps.SessionDep,
    project_id: int,
    classifier_id: int,
    config_id: int,
) -> None:
    """Delete an intermediatory class to keyword config."""
    crud.delete_intermediatory_class_to_keyword_config(
        session=session,
        project_id=project_id,
        classifier_id=classifier_id,
        intermediatory_class_to_keyword_config_id=config_id,
    )
