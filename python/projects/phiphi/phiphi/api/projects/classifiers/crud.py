"""CRUD operations for the classifiers API."""
from datetime import datetime

import sqlalchemy.orm

from phiphi.api.projects.classifiers import models, schemas


def create_classifier(
    session: sqlalchemy.orm.Session, classifier: schemas.ClassifierCreate
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

    initial_version = models.ClassifierVersions(
        classifier_id=orm_classifier.id,
        classes_dict=classifier.classes_dict,
        params=classifier.params,
    )
    session.add(initial_version)
    session.commit()
    session.refresh(initial_version)

    return schemas.ClassifierResponse(
        id=orm_classifier.id,
        project_id=orm_classifier.project_id,
        name=orm_classifier.name,
        type=orm_classifier.type,
        archived_at=orm_classifier.archived_at,
        version_id=initial_version.version_id,
        classes_dict=initial_version.classes_dict,
        params=initial_version.params,
        created_at=orm_classifier.created_at,
        updated_at=orm_classifier.updated_at,
        version_created_at=initial_version.created_at,
        version_updated_at=initial_version.updated_at,
    )


def get_classifier(
    session: sqlalchemy.orm.Session, classifier_id: int
) -> schemas.ClassifierResponse | None:
    """Get a classifier with its latest version."""
    orm_classifier = (
        session.query(models.Classifiers).filter(models.Classifiers.id == classifier_id).first()
    )
    if orm_classifier is None:
        return None

    latest_version = orm_classifier.latest_version
    if latest_version is None:
        return None

    return schemas.ClassifierResponse(
        id=orm_classifier.id,
        project_id=orm_classifier.project_id,
        name=orm_classifier.name,
        type=orm_classifier.type,
        archived_at=orm_classifier.archived_at,
        version_id=latest_version.version_id,
        classes_dict=latest_version.classes_dict,
        params=latest_version.params,
        created_at=orm_classifier.created_at,
        updated_at=orm_classifier.updated_at,
        version_created_at=latest_version.created_at,
        version_updated_at=latest_version.updated_at,
    )


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

    classifiers = []
    for orm_classifier in orm_classifiers:
        latest_version = orm_classifier.latest_version
        classifiers.append(
            schemas.ClassifierResponse(
                id=orm_classifier.id,
                project_id=orm_classifier.project_id,
                name=orm_classifier.name,
                type=orm_classifier.type,
                archived_at=orm_classifier.archived_at,
                version_id=latest_version.version_id,
                classes_dict=latest_version.classes_dict,
                params=latest_version.params,
                created_at=orm_classifier.created_at,
                updated_at=orm_classifier.updated_at,
                version_created_at=latest_version.created_at,
                version_updated_at=latest_version.updated_at,
            )
        )
    return classifiers


def update_classifier_version(
    session: sqlalchemy.orm.Session,
    classifier_id: int,
    update_data: schemas.ClassifierUpdateVersion,
) -> schemas.ClassifierResponse | None:
    """Update the version of a classifier."""
    orm_classifier = (
        session.query(models.Classifiers).filter(models.Classifiers.id == classifier_id).first()
    )
    if orm_classifier is None:
        return None

    new_version = models.ClassifierVersions(
        classifier_id=classifier_id,
        classes_dict=update_data.classes_dict
        if update_data.classes_dict
        else orm_classifier.latest_version.classes_dict,
        params=update_data.params if update_data.params else orm_classifier.latest_version.params,
    )
    session.add(new_version)
    session.commit()
    session.refresh(new_version)

    return schemas.ClassifierResponse(
        id=orm_classifier.id,
        project_id=orm_classifier.project_id,
        name=orm_classifier.name,
        type=orm_classifier.type,
        archived_at=orm_classifier.archived_at,
        version_id=new_version.version_id,
        classes_dict=new_version.classes_dict,
        params=new_version.params,
        created_at=orm_classifier.created_at,
        updated_at=orm_classifier.updated_at,
        version_created_at=new_version.created_at,
        version_updated_at=new_version.updated_at,
    )


def archive_classifier(
    session: sqlalchemy.orm.Session, classifier_id: int
) -> schemas.ClassifierResponse | None:
    """Archive (delete) a classifier.

    Sets the archived_at col to current datetime.
    """
    orm_classifier = (
        session.query(models.Classifiers).filter(models.Classifiers.id == classifier_id).first()
    )
    if orm_classifier is None:
        return None
    elif orm_classifier:
        orm_classifier.archived_at = datetime.now()
        session.commit()
        session.refresh(orm_classifier)

    latest_version = orm_classifier.latest_version
    if latest_version is None:
        return None

    return schemas.ClassifierResponse(
        id=orm_classifier.id,
        project_id=orm_classifier.project_id,
        name=orm_classifier.name,
        type=orm_classifier.type,
        archived_at=orm_classifier.archived_at,
        version_id=latest_version.version_id,
        classes_dict=latest_version.classes_dict,
        params=latest_version.params,
        created_at=orm_classifier.created_at,
        updated_at=orm_classifier.updated_at,
        version_created_at=latest_version.created_at,
        version_updated_at=latest_version.updated_at,
    )
