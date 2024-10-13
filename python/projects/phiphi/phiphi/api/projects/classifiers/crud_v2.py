"""CRUD operations for classifiers version 2.

At somepoint this will replace the current CRUD operations in `crud.py`.
"""
import datetime

import sqlalchemy.orm

from phiphi.api import exceptions
from phiphi.api.projects.classifiers import base_schemas, models, response_schemas
from phiphi.api.projects.job_runs import crud as job_run_crud
from phiphi.api.projects.job_runs import schemas as job_run_schemas


def create_classifier(
    session: sqlalchemy.orm.Session,
    project_id: int,
    classifier_type: base_schemas.ClassifierType,
    classifier_create: base_schemas.ClassifierCreate,
) -> response_schemas.Classifier:
    """Create a new classifier with an initial version.

    To make the versioning more transparent we only create versions for a classifier when
    `create_version` is called.
    """
    orm_classifier = models.Classifiers(
        project_id=project_id,
        name=classifier_create.name,
        type=classifier_type,
        archived_at=None,
    )
    session.add(orm_classifier)
    session.commit()
    session.refresh(orm_classifier)

    for class_create in classifier_create.intermediatory_classes:
        orm_intermediate_class = models.IntermediatoryClasses(
            classifier_id=orm_classifier.id,
            name=class_create.name,
            description=class_create.description,
        )
        session.add(orm_intermediate_class)

    session.commit()
    session.refresh(orm_classifier)
    return response_schemas.classifier_adapter.validate_python(orm_classifier)


def get_class_dict(
    session: sqlalchemy.orm.Session,
    orm_classifier: models.Classifiers,
) -> base_schemas.ClassesDictType:
    """Get the classes dict for a classifier.

    This will return a dictionary of the classes for a classifier.

    Args:
        session: SQLAlchemy session.
        orm_classifier: Classifier ORM. Using a classifier ORM rather then just the id to show that
            the classifier has to exist.

    Returns:
        ClassesDictType
    """
    list_intermediatory_classes = (
        session.query(models.IntermediatoryClasses)
        .filter(models.IntermediatoryClasses.classifier_id == orm_classifier.id)
        .all()
    )

    classes_dict: base_schemas.ClassesDictType = {}

    # Due to the unique index on intermediatory_classes table we know there is one name per class
    for intermediate_class in list_intermediatory_classes:
        classes_dict[intermediate_class.name] = intermediate_class.description

    return classes_dict


def get_orm_classifier(
    session: sqlalchemy.orm.Session,
    project_id: int,
    classifier_id: int,
) -> models.Classifiers | None:
    """Get a classifier ORM."""
    return (
        session.query(models.Classifiers)
        .filter(models.Classifiers.project_id == project_id)
        .filter(models.Classifiers.id == classifier_id)
        .one_or_none()
    )


def get_classifier(
    session: sqlalchemy.orm.Session,
    project_id: int,
    classifier_id: int,
) -> response_schemas.Classifier | None:
    """Get a classifier with its latest version."""
    orm_classifier = get_orm_classifier(session, project_id, classifier_id)

    if orm_classifier is None:
        return None

    return response_schemas.classifier_adapter.validate_python(orm_classifier)


def get_classifiers(
    session: sqlalchemy.orm.Session,
    project_id: int,
    start: int = 0,
    end: int = 10,
    include_archived: bool = True,
) -> list[response_schemas.OptimisedClassifier]:
    """Get a list of classifiers for a project."""
    query = (
        session.query(models.Classifiers)
        .filter(models.Classifiers.project_id == project_id)
        .order_by(models.Classifiers.id.desc())
        .slice(start, end)
    )
    if not include_archived:
        query = query.filter(models.Classifiers.archived_at.is_(None))

    return [
        response_schemas.OptimisedClassifier.model_validate(orm_classifier)
        for orm_classifier in query.all()
    ]


def patch_classifier(
    session: sqlalchemy.orm.Session,
    project_id: int,
    classifier_id: int,
    classifier_patch: base_schemas.ClassifierPatch,
) -> response_schemas.Classifier:
    """Patch a classifier."""
    orm_classifier = get_orm_classifier(session, project_id, classifier_id)

    if orm_classifier is None:
        raise exceptions.ClassifierNotFound()

    if orm_classifier.archived_at is not None:
        raise exceptions.ClassifierArchived()

    for key, value in classifier_patch.dict(exclude_unset=True).items():
        setattr(orm_classifier, key, value)

    session.commit()
    session.refresh(orm_classifier)
    return response_schemas.classifier_adapter.validate_python(orm_classifier)


def archive_classifier(
    session: sqlalchemy.orm.Session,
    project_id: int,
    classifier_id: int,
) -> models.Classifiers:
    """Archive a classifier."""
    orm_classifier = get_orm_classifier(session, project_id, classifier_id)

    if orm_classifier is None:
        raise exceptions.ClassifierNotFound()

    orm_classifier.archived_at = datetime.datetime.utcnow()
    session.commit()
    session.refresh(orm_classifier)

    return orm_classifier


async def archive_classifier_run_archive_job(
    session: sqlalchemy.orm.Session,
    project_id: int,
    classifier_id: int,
) -> response_schemas.Classifier:
    """Archive a classifier and run the classifier archive job."""
    orm_classifier = archive_classifier(session, project_id, classifier_id)

    _ = await job_run_crud.create_and_run_job_run(
        session,
        project_id,
        job_run_schemas.JobRunCreate(
            foreign_id=orm_classifier.id,
            foreign_job_type=job_run_schemas.ForeignJobType.classifier_archive,
        ),
    )
    return response_schemas.classifier_adapter.validate_python(orm_classifier)


def restore_classifier(
    session: sqlalchemy.orm.Session,
    project_id: int,
    classifier_id: int,
) -> response_schemas.Classifier:
    """Restore a classifier.

    This will set the `archived_at` field to `None` and run the `restore_classifier` job.

    The job will be responsible for restoring the classifier and applying the latest_version.

    Args:
        session: SQLAlchemy session.
        project_id: Project ID.
        classifier_id: Classifier ID.

    Returns:
        The restored classifier.

    Raises:
        ClassifierNotFound: If the classifier does not exist.
    """
    orm_classifier = get_orm_classifier(session, project_id, classifier_id)

    if orm_classifier is None:
        raise exceptions.ClassifierNotFound()

    orm_classifier.archived_at = None
    session.commit()
    session.refresh(orm_classifier)
    # TODO: add the restore_classifier job run that should be kicked off but not waited for.
    return response_schemas.classifier_adapter.validate_python(orm_classifier)
