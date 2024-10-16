"""Crud for keyword_match."""
import sqlalchemy as sa

from phiphi.api import exceptions
from phiphi.api.projects.classifiers import crud_v2 as crud
from phiphi.api.projects.classifiers import models as classifiers_models
from phiphi.api.projects.classifiers.keyword_match import models, schemas

UNIQUE_ERROR_MESSAGE = "The class to keyword match configuration already exists."


def create_version(
    session: sa.orm.Session,
    project_id: int,
    classifier_id: int,
) -> schemas.KeywordMatchVersionResponse:
    """Create a keyword match version."""
    orm_classifier = crud.get_orm_classifier(session, project_id, classifier_id)
    if orm_classifier is None:
        raise exceptions.ClassifierNotFound()

    classes = crud.get_classes(session, orm_classifier)

    orm_version = classifiers_models.ClassifierVersions(
        classifier_id=orm_classifier.id,
        classes=[class_label.model_dump() for class_label in classes],
        # This needs to be implemented in the future
        params={"class_to_keyword_configs": []},
    )
    session.add(orm_version)
    session.commit()
    session.refresh(orm_version)
    return schemas.KeywordMatchVersionResponse.model_validate(orm_version)


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
            raise exceptions.HttpException404()

        for key, value in intermediatory_class_to_keyword_config.model_dump(
            exclude_unset=True
        ).items():
            setattr(orm_intermediatory_class_to_keyword_config, key, value)

        session.commit()

    session.refresh(orm_intermediatory_class_to_keyword_config)
    return schemas.IntermediatoryClassToKeywordConfigResponse.model_validate(
        orm_intermediatory_class_to_keyword_config
    )
