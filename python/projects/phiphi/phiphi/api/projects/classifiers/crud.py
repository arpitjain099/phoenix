"""CRUD operations for the classifiers API."""
from datetime import datetime

import sqlalchemy.orm

from phiphi.api.projects.classifiers import models, schemas


def create_classifier(
    session: sqlalchemy.orm.Session,
    classifier: schemas.ClassifierCreate,
    version: schemas.ClassifierVersionCreate,
) -> schemas.ClassifierResponse:
    """Create a new classifier with an initial version."""
    orm_classifier = models.Classifiers(
        project_id=classifier.project_id,
        name=classifier.name,
        type=classifier.type,
        archived_at=None,
    )
    session.add(orm_classifier)
    session.commit()
    session.refresh(orm_classifier)

    orm_initial_version = models.ClassifierVersions(
        classifier_id=orm_classifier.id,
        classes=version.classes,
        params=version.params,
    )
    session.add(orm_initial_version)
    session.commit()
    session.refresh(orm_initial_version)

    return schemas.ClassifierResponse.model_validate(orm_classifier)


def get_classifier(
    session: sqlalchemy.orm.Session, classifier_id: int
) -> schemas.ClassifierResponse | None:
    """Get a classifier with its latest version."""
    orm_classifier = (
        session.query(models.Classifiers).filter(models.Classifiers.id == classifier_id).first()
    )

    if orm_classifier is None:
        return None

    return schemas.ClassifierResponse.model_validate(orm_classifier)


def get_classifiers(
    session: sqlalchemy.orm.Session,
    project_id: int,
    include_archived: bool = False,
    active_classifiers_only: bool = True,
) -> list[schemas.ClassifierResponse]:
    """Get a list of classifiers for a project."""
    query = session.query(models.Classifiers).filter(models.Classifiers.project_id == project_id)

    if not include_archived:
        query = query.filter(models.Classifiers.archived_at.is_(None))

    orm_classifiers = query.order_by(models.Classifiers.id.desc()).all()

    # Filter out classifiers without a latest version
    # Pipelines classifiers should always have a latest version
    if active_classifiers_only:
        orm_classifiers = [
            classifier for classifier in orm_classifiers if classifier.latest_version is not None
        ]

    return [
        schemas.ClassifierResponse.model_validate(orm_classifier)
        for orm_classifier in orm_classifiers
    ]


def classifier_version_create(
    session: sqlalchemy.orm.Session,
    classifier_id: int,
    version: schemas.ClassifierVersionCreate,
) -> schemas.ClassifierResponse | None:
    """Create a new version of a classifier."""
    orm_classifier = (
        session.query(models.Classifiers).filter(models.Classifiers.id == classifier_id).first()
    )
    if orm_classifier is None:
        return None

    new_version = models.ClassifierVersions(
        classifier_id=classifier_id,
        classes=version.classes,
        params=version.params,
    )
    session.add(new_version)
    session.commit()
    session.refresh(new_version)

    return schemas.ClassifierResponse.model_validate(orm_classifier)


def archive_classifier(
    session: sqlalchemy.orm.Session, classifier_id: int
) -> schemas.ClassifierResponse | None:
    """Archive (soft delete) a classifier by setting the archived_at field."""
    orm_classifier = (
        session.query(models.Classifiers).filter(models.Classifiers.id == classifier_id).first()
    )

    if orm_classifier is None:
        return None

    orm_classifier.archived_at = datetime.now()
    session.commit()
    session.refresh(orm_classifier)

    return schemas.ClassifierResponse.model_validate(orm_classifier)
