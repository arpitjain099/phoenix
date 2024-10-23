"""Crud functionality for manual post authors."""
import sqlalchemy as sa

from phiphi.api import exceptions
from phiphi.api.projects.classifiers import base_schemas, crud
from phiphi.api.projects.classifiers import models as classifiers_models
from phiphi.api.projects.classifiers.manual_post_authors import models, schemas

UNIQUE_ERROR_MESSAGE = "The author id and class id pair already exists."


def create_intermediatory_classified_post_authors(
    session: sa.orm.Session,
    project_id: int,
    classifier_id: int,
    create_obj: schemas.IntermediatoryClassifiedPostAuthorsCreate,
) -> schemas.IntermediatoryClassifiedPostAuthorsResponse:
    """Create an intermediatory classified post author."""
    with crud.get_orm_classifier_with_edited_context(
        session=session, project_id=project_id, classifier_id=classifier_id
    ) as orm_classifier:
        if orm_classifier.type != base_schemas.ClassifierType.manual_post_authors:
            raise exceptions.HttpException400("Invalid classifier type")

        orm_intermediate_class = session.query(classifiers_models.IntermediatoryClasses).get(
            create_obj.class_id
        )

        if orm_intermediate_class is None:
            raise exceptions.IntermediatoryClassNotFound()

        try:
            orm = models.IntermediatoryClassifiedPostAuthors(
                classifier_id=orm_classifier.id,
                class_id=create_obj.class_id,
                phoenix_platform_message_author_id=create_obj.phoenix_platform_message_author_id,
            )
            session.add(orm)
            session.commit()
        except sa.exc.IntegrityError as e:
            session.rollback()
            if "unique constraint" in str(e):
                raise exceptions.HttpException400(UNIQUE_ERROR_MESSAGE)
            raise exceptions.UnknownIntegrityError()
    session.refresh(orm_classifier)
    return schemas.IntermediatoryClassifiedPostAuthorsResponse.model_validate(orm)


def delete_intermediatory_classified_post_author(
    session: sa.orm.Session,
    project_id: int,
    classifier_id: int,
    classified_post_author_id: int,
) -> None:
    """Delete an intermediatory classified post author."""
    with crud.get_orm_classifier_with_edited_context(
        session=session, project_id=project_id, classifier_id=classifier_id
    ) as orm_classifier:
        if orm_classifier.type != base_schemas.ClassifierType.manual_post_authors:
            raise exceptions.HttpException400("Invalid classifier type")

        orm = (
            session.query(models.IntermediatoryClassifiedPostAuthors)
            .filter(models.IntermediatoryClassifiedPostAuthors.id == classified_post_author_id)
            .first()
        )
        if orm is None:
            raise exceptions.HttpException404("Intermediatory classified post author not found")
        session.delete(orm)
        session.commit()
    session.refresh(orm_classifier)
    return None
