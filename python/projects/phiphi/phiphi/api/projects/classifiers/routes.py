"""Classifier routes."""
import fastapi

from phiphi.api import deps, exceptions
from phiphi.api.projects.classifiers import base_schemas, response_schemas
from phiphi.api.projects.classifiers import crud_v2 as crud
from phiphi.api.projects.classifiers.keyword_match import routes as keyword_match_routes

router = fastapi.APIRouter()
router.include_router(keyword_match_routes.router)


@router.get(
    "/projects/{project_id}/classifiers/{classifier_id}",
    response_model=response_schemas.ClassifierDetail,
)
def get_classifier(
    session: deps.SessionDep,
    project_id: int,
    classifier_id: int,
) -> response_schemas.ClassifierDetail:
    """Get a classifier."""
    classifier = crud.get_classifier(
        session=session, project_id=project_id, classifier_id=classifier_id
    )
    if classifier is None:
        raise exceptions.ClassifierNotFound()
    return classifier


@router.get(
    "/projects/{project_id}/classifiers", response_model=list[response_schemas.OptimisedClassifier]
)
def get_classifiers(
    session: deps.SessionDep,
    project_id: int,
    start: int = 0,
    end: int = 100,
) -> list[response_schemas.OptimisedClassifier]:
    """Get classifiers."""
    return crud.get_classifiers(session=session, project_id=project_id, start=start, end=end)


@router.patch(
    "/projects/{project_id}/classifiers/{classifier_id}",
    response_model=response_schemas.ClassifierDetail,
)
def patch_classifier(
    session: deps.SessionDep,
    project_id: int,
    classifier_id: int,
    classifier_patch: base_schemas.ClassifierPatch,
) -> response_schemas.ClassifierDetail:
    """Patch a classifier."""
    classifier = crud.patch_classifier(
        session=session,
        project_id=project_id,
        classifier_id=classifier_id,
        classifier_patch=classifier_patch,
    )
    return classifier


@router.post(
    "/projects/{project_id}/classifiers/{classifier_id}/archive",
    response_model=response_schemas.ClassifierDetail,
)
async def archive_classifier(
    session: deps.SessionDep,
    project_id: int,
    classifier_id: int,
) -> response_schemas.ClassifierDetail:
    """Archive a classifier."""
    classifier = await crud.archive_classifier_run_archive_job(
        session=session, project_id=project_id, classifier_id=classifier_id
    )
    return classifier


@router.post(
    "/projects/{project_id}/classifiers/{classifier_id}/restore",
    response_model=response_schemas.ClassifierDetail,
)
async def restore_classifier(
    session: deps.SessionDep,
    project_id: int,
    classifier_id: int,
) -> response_schemas.ClassifierDetail:
    """Restore a classifier."""
    classifier = await crud.restore_classifier_run_restore_job(
        session=session, project_id=project_id, classifier_id=classifier_id
    )
    return classifier
