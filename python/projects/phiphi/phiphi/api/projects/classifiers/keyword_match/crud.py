"""Crud for keyword_match."""
import sqlalchemy as sa

from phiphi.api import exceptions
from phiphi.api.projects.classifiers import crud_v2 as crud
from phiphi.api.projects.classifiers import models
from phiphi.api.projects.classifiers.keyword_match import schemas


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

    orm_version = models.ClassifierVersions(
        classifier_id=orm_classifier.id,
        classes=[class_label.model_dump() for class_label in classes],
        # This needs to be implemented in the future
        params={"class_to_keyword_configs": []},
    )
    session.add(orm_version)
    session.commit()
    session.refresh(orm_version)
    return schemas.KeywordMatchVersionResponse.model_validate(orm_version)
