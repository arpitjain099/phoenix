"""CRUD operations for classifiers version 2.

At somepoint this will replace the current CRUD operations in `crud.py`.
"""
import sqlalchemy.orm

from phiphi.api.projects.classifiers import base_schemas, models, response_schemas


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


def get_classifier(
    session: sqlalchemy.orm.Session,
    project_id: int,
    classifier_id: int,
) -> response_schemas.Classifier | None:
    """Get a classifier with its latest version."""
    orm_classifier = (
        session.query(models.Classifiers)
        .filter(models.Classifiers.project_id == project_id)
        .filter(models.Classifiers.id == classifier_id)
        .first()
    )

    if orm_classifier is None:
        return None

    return response_schemas.classifier_adapter.validate_python(orm_classifier)


def get_classifiers(
    session: sqlalchemy.orm.Session,
    project_id: int,
    start: int = 0,
    end: int = 10,
    include_archived: bool = True,
) -> list[response_schemas.ClassifierList]:
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
        response_schemas.ClassifierList.model_validate(orm_classifier)
        for orm_classifier in query.all()
    ]
