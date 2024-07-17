"""CRUD functionality for classifiers tables."""
from datetime import datetime

import sqlalchemy.orm

from phiphi.api.projects.classifiers import models, schemas


def create_classifier(
    session: sqlalchemy.orm.Session, classifier: schemas.ClassifierCreate
) -> schemas.ClassifierResponse:
    """Create a new classifier."""
    db_classifier = models.Classifiers(
        **classifier.dict(), created_at=datetime.now(), archived_at=None
    )
    session.add(db_classifier)
    session.commit()
    session.refresh(db_classifier)
    return schemas.ClassifierResponse.model_validate(db_classifier)


def get_classifier(
    session: sqlalchemy.orm.Session, classifier_id: int
) -> schemas.ClassifierResponse | None:
    """Get a classifier."""
    db_classifier = (
        session.query(models.Classifiers).filter(models.Classifiers.id == classifier_id).first()
    )

    if db_classifier is None:
        return None
    return schemas.ClassifierResponse.model_validate(db_classifier)


def get_classifiers(
    session: sqlalchemy.orm.Session,
    project_id: int,
    included_deleted: bool = False,
) -> list[schemas.ClassifierResponse]:
    """Get classifiers."""
    query = session.query(models.Classifiers).filter(models.Classifiers.project_id == project_id)
    if not included_deleted:
        query = query.filter(models.Classifiers.archived_at.is_(None))
    db_classifiers = query.order_by(models.Classifiers.id.desc()).all()
    return [
        schemas.ClassifierResponse.model_validate(db_classifier)
        for db_classifier in db_classifiers
    ]


def archive_classifier(
    session: sqlalchemy.orm.Session, classifier_id: int
) -> schemas.ClassifierResponse:
    """Archive (delete) a classifier.

    Sets the archived_at col to current datetime.
    """
    db_classifier = (
        session.query(models.Classifiers).filter(models.Classifiers.id == classifier_id).first()
    )
    if db_classifier:
        db_classifier.archived_at = datetime.now()
        session.commit()
        session.refresh(db_classifier)
    return schemas.ClassifierResponse.model_validate(db_classifier)


def create_class(
    session: sqlalchemy.orm.Session, class_: schemas.ClassCreate
) -> schemas.ClassResponse:
    """Create a new class."""
    db_class = models.Classes(**class_.dict())
    session.add(db_class)
    session.commit()
    session.refresh(db_class)
    return schemas.ClassResponse.model_validate(db_class)


def get_class(session: sqlalchemy.orm.Session, class_id: int) -> schemas.ClassResponse | None:
    """Get a class."""
    db_class = session.query(models.Classes).filter(models.Classes.id == class_id).first()
    if db_class is None:
        return None
    return schemas.ClassResponse.model_validate(db_class)


def get_classes(
    session: sqlalchemy.orm.Session,
    project_id: int,
) -> list[schemas.ClassResponse]:
    """Get classes."""
    db_classes = (
        session.query(models.Classes).filter(models.Classes.project_id == project_id).all()
    )
    return [schemas.ClassResponse.model_validate(db_class) for db_class in db_classes]


def delete_class(session: sqlalchemy.orm.Session, class_id: int) -> None:
    """Delete a class."""
    db_class = session.query(models.Classes).filter(models.Classes.id == class_id).first()
    if db_class:
        session.delete(db_class)
        session.commit()


def update_class(
    session: sqlalchemy.orm.Session, class_id: int, class_: schemas.ClassUpdate
) -> schemas.ClassResponse | None:
    """Update a class."""
    db_class = session.get(models.Classes, class_id)
    if db_class:
        for field, value in class_.dict(exclude={"id"}).items():
            setattr(db_class, field, value)
        session.commit()
        session.refresh(db_class)
    return schemas.ClassResponse.model_validate(db_class)
