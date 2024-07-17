"""CRUD functionality for classifiers tables."""
from datetime import datetime

import sqlalchemy.orm

from phiphi.api.projects.classifiers import models, schemas


def create_classifier(
    session: sqlalchemy.orm.Session, classifier: schemas.ClassifierCreate
) -> schemas.ClassifierResponse:
    """Create a new classifier."""
    orm_classifier = models.Classifiers(
        **classifier.dict(), created_at=datetime.now(), archived_at=None
    )
    session.add(orm_classifier)
    session.commit()
    session.refresh(orm_classifier)
    return schemas.ClassifierResponse.model_validate(orm_classifier)


def get_classifier(
    session: sqlalchemy.orm.Session, classifier_id: int
) -> schemas.ClassifierResponse | None:
    """Get a classifier."""
    orm_classifier = (
        session.query(models.Classifiers).filter(models.Classifiers.id == classifier_id).first()
    )

    if orm_classifier is None:
        return None
    return schemas.ClassifierResponse.model_validate(orm_classifier)


def get_classifiers(
    session: sqlalchemy.orm.Session,
    project_id: int,
    included_deleted: bool = False,
) -> list[schemas.ClassifierResponse]:
    """Get classifiers."""
    query = session.query(models.Classifiers).filter(models.Classifiers.project_id == project_id)
    if not included_deleted:
        query = query.filter(models.Classifiers.archived_at.is_(None))
    orm_classifiers = query.order_by(models.Classifiers.id.desc()).all()
    return [
        schemas.ClassifierResponse.model_validate(orm_classifier)
        for orm_classifier in orm_classifiers
    ]


def archive_classifier(
    session: sqlalchemy.orm.Session, classifier_id: int
) -> schemas.ClassifierResponse:
    """Archive (delete) a classifier.

    Sets the archived_at col to current datetime.
    """
    orm_classifier = (
        session.query(models.Classifiers).filter(models.Classifiers.id == classifier_id).first()
    )
    if orm_classifier:
        orm_classifier.archived_at = datetime.now()
        session.commit()
        session.refresh(orm_classifier)
    return schemas.ClassifierResponse.model_validate(orm_classifier)


def create_class(
    session: sqlalchemy.orm.Session, class_: schemas.ClassCreate
) -> schemas.ClassResponse:
    """Create a new class."""
    orm_class = models.Classes(**class_.dict(), last_updated_at=datetime.now())
    session.add(orm_class)
    session.commit()
    session.refresh(orm_class)
    return schemas.ClassResponse.model_validate(orm_class)


def get_class(session: sqlalchemy.orm.Session, class_id: int) -> schemas.ClassResponse | None:
    """Get a class."""
    orm_class = session.query(models.Classes).filter(models.Classes.id == class_id).first()
    if orm_class is None:
        return None
    return schemas.ClassResponse.model_validate(orm_class)


def get_classes(
    session: sqlalchemy.orm.Session,
    project_id: int,
) -> list[schemas.ClassResponse]:
    """Get classes."""
    orm_classes = (
        session.query(models.Classes).filter(models.Classes.project_id == project_id).all()
    )
    return [schemas.ClassResponse.model_validate(orm_class) for orm_class in orm_classes]


def delete_class(session: sqlalchemy.orm.Session, class_id: int) -> None:
    """Delete a class."""
    orm_class = session.query(models.Classes).filter(models.Classes.id == class_id).first()
    if orm_class:
        session.delete(orm_class)
        session.commit()


def update_class(
    session: sqlalchemy.orm.Session, class_id: int, class_: schemas.ClassUpdate
) -> schemas.ClassResponse | None:
    """Update a class."""
    orm_class = session.get(models.Classes, class_id)
    if orm_class:
        for field, value in class_.dict(exclude={"id"}).items():
            setattr(orm_class, field, value)
        orm_class.last_updated_at = datetime.now()
        session.commit()
        session.refresh(orm_class)
    return schemas.ClassResponse.model_validate(orm_class)
