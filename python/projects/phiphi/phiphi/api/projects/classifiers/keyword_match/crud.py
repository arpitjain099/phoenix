"""Crud for keyword_match."""
import sqlalchemy as sa

from phiphi.api import exceptions
from phiphi.api.projects.classifiers import base_schemas as classifiers_base_schemas
from phiphi.api.projects.classifiers import crud
from phiphi.api.projects.classifiers import models as classifiers_models
from phiphi.api.projects.classifiers.keyword_match import models, schemas
from phiphi.api.projects.job_runs import crud as job_run_crud
from phiphi.api.projects.job_runs import schemas as job_run_schemas

UNIQUE_ERROR_MESSAGE = "The class to keyword match configuration already exists."
NOT_FOUND_ERROR_MESSAGE = "The class to keyword match configuration does not exist."


def create_version(
    session: sa.orm.Session,
    project_id: int,
    classifier_id: int,
) -> schemas.KeywordMatchVersionResponse:
    """Create a keyword match version."""
    orm_classifier = crud.get_orm_classifier(session, project_id, classifier_id)
    if orm_classifier is None:
        raise exceptions.ClassifierNotFound()

    if orm_classifier.type != classifiers_base_schemas.ClassifierType.keyword_match:
        raise exceptions.HttpException400("The classifier is not a keyword match classifier.")

    classes = crud.get_classes(session, orm_classifier)
    params = get_keyword_match_params(session, orm_classifier)

    orm_version = classifiers_models.ClassifierVersions(
        classifier_id=orm_classifier.id,
        classes=[class_label.model_dump() for class_label in classes],
        params=params,
    )
    session.add(orm_version)
    session.commit()
    session.refresh(orm_version)
    return schemas.KeywordMatchVersionResponse.model_validate(orm_version)


def get_keyword_match_params(
    session: sa.orm.Session,
    orm_classifier: classifiers_models.Classifiers,
) -> schemas.KeywordMatchParams:
    """Get keyword match params."""
    all_configs = orm_classifier.intermediatory_class_to_keyword_configs
    class_to_keyword_configs = []
    for orm_intermediatory_class_to_keyword_config in all_configs:
        class_to_keyword_config = schemas.ClassToKeywordConfig(
            class_name=orm_intermediatory_class_to_keyword_config.class_name,
            musts=orm_intermediatory_class_to_keyword_config.musts,
            nots=orm_intermediatory_class_to_keyword_config.nots,
        )
        class_to_keyword_configs.append(class_to_keyword_config)
    return schemas.KeywordMatchParams(class_to_keyword_configs=class_to_keyword_configs)


async def create_version_and_run(
    session: sa.orm.Session,
    project_id: int,
    classifier_id: int,
) -> schemas.KeywordMatchClassifierDetail:
    """Create a keyword match version and run."""
    orm_classifier = crud.get_orm_classifier(session, project_id, classifier_id)
    if orm_classifier is None:
        raise exceptions.ClassifierNotFound()
    _ = create_version(session, project_id, classifier_id)
    _ = await job_run_crud.create_and_run_job_run(
        session,
        project_id,
        job_run_schemas.JobRunCreate(
            foreign_id=orm_classifier.id,
            foreign_job_type=job_run_schemas.ForeignJobType.classify_tabulate,
        ),
    )
    session.refresh(orm_classifier)
    return schemas.KeywordMatchClassifierDetail.model_validate(obj=orm_classifier)


def create_intermediatory_class_to_keyword_config(
    session: sa.orm.Session,
    project_id: int,
    classifier_id: int,
    intermediatory_class_to_keyword_config: schemas.IntermediatoryClassToKeywordConfigCreate,
) -> schemas.IntermediatoryClassToKeywordConfigResponse:
    """Create an intermediatory class to keyword config."""
    with crud.get_orm_classifier_with_edited_context(
        session, project_id, classifier_id
    ) as orm_classifier:
        try:
            # Attempt to add an object that may violate the unique constraint
            orm_intermediatory_class_to_keyword_config = models.IntermediatoryClassToKeywordConfig(
                classifier_id=orm_classifier.id,
                class_id=intermediatory_class_to_keyword_config.class_id,
                musts=intermediatory_class_to_keyword_config.musts,
                nots=intermediatory_class_to_keyword_config.nots,
            )
            session.add(orm_intermediatory_class_to_keyword_config)
            session.commit()
        except sa.exc.IntegrityError as e:
            session.rollback()
            if "unique constraint" in str(e):
                raise exceptions.HttpException400(UNIQUE_ERROR_MESSAGE)
            raise exceptions.UnknownIntegrityError()

    session.refresh(orm_intermediatory_class_to_keyword_config)
    return schemas.IntermediatoryClassToKeywordConfigResponse.model_validate(
        orm_intermediatory_class_to_keyword_config
    )


def patch_intermediatory_class_to_keyword_config(
    session: sa.orm.Session,
    project_id: int,
    classifier_id: int,
    intermediatory_class_to_keyword_config_id: int,
    intermediatory_class_to_keyword_config: schemas.IntermediatoryClassToKeywordConfigPatch,
) -> schemas.IntermediatoryClassToKeywordConfigResponse:
    """Patch an intermediatory class to keyword config."""
    with crud.get_orm_classifier_with_edited_context(
        session, project_id, classifier_id
    ) as orm_classifier:
        orm_intermediatory_class_to_keyword_config = (
            session.query(models.IntermediatoryClassToKeywordConfig)
            .filter(
                models.IntermediatoryClassToKeywordConfig.id
                == intermediatory_class_to_keyword_config_id,
                models.IntermediatoryClassToKeywordConfig.classifier_id == orm_classifier.id,
            )
            .one_or_none()
        )
        if orm_intermediatory_class_to_keyword_config is None:
            raise exceptions.HttpException404(NOT_FOUND_ERROR_MESSAGE)

        try:
            for key, value in intermediatory_class_to_keyword_config.model_dump(
                exclude_unset=True
            ).items():
                setattr(orm_intermediatory_class_to_keyword_config, key, value)

            session.commit()
        except sa.exc.IntegrityError as e:
            session.rollback()
            if "unique constraint" in str(e):
                raise exceptions.HttpException400(UNIQUE_ERROR_MESSAGE)
            raise exceptions.UnknownIntegrityError()

    session.refresh(orm_intermediatory_class_to_keyword_config)
    return schemas.IntermediatoryClassToKeywordConfigResponse.model_validate(
        orm_intermediatory_class_to_keyword_config
    )


def delete_intermediatory_class_to_keyword_config(
    session: sa.orm.Session,
    project_id: int,
    classifier_id: int,
    intermediatory_class_to_keyword_config_id: int,
) -> None:
    """Delete an intermediatory class to keyword config."""
    with crud.get_orm_classifier_with_edited_context(
        session, project_id, classifier_id
    ) as orm_classifier:
        orm_intermediatory_class_to_keyword_config = (
            session.query(models.IntermediatoryClassToKeywordConfig)
            .filter(
                models.IntermediatoryClassToKeywordConfig.id
                == intermediatory_class_to_keyword_config_id,
                models.IntermediatoryClassToKeywordConfig.classifier_id == orm_classifier.id,
            )
            .one_or_none()
        )
        if orm_intermediatory_class_to_keyword_config is None:
            raise exceptions.HttpException404(NOT_FOUND_ERROR_MESSAGE)

        session.delete(orm_intermediatory_class_to_keyword_config)
        session.commit()
