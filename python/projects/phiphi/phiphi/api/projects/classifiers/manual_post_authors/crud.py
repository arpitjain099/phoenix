"""Crud functionality for manual post authors."""
import sqlalchemy as sa

from phiphi.api import exceptions
from phiphi.api.projects.classifiers import base_schemas, crud
from phiphi.api.projects.classifiers.manual_post_authors import models, schemas


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

        orm_intermediatory_classified_post_authors = models.IntermediatoryClassifiedPostAuthors(
            classifier_id=orm_classifier.id,
            class_id=create_obj.class_id,
            phoenix_platform_message_author_id=create_obj.phoenix_platform_message_author_id,
        )
        session.add(orm_intermediatory_classified_post_authors)
        session.commit()
    session.refresh(orm_classifier)
    return schemas.IntermediatoryClassifiedPostAuthorsResponse.model_validate(
        orm_intermediatory_classified_post_authors
    )
