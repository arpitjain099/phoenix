"""Child CRUD operations for the classifiers API.

At some point it might be best to integrate this into the main classifier CRUD operations.
"""
import sqlalchemy.orm

from phiphi.api.projects.classifiers import base_schemas, models


def create_classifier(
    session: sqlalchemy.orm.Session,
    project_id: int,
    classifier_type: base_schemas.ClassifierType,
    classifier_create: base_schemas.ClassifierCreate,
) -> None:
    """Create a new classifier with an initial version."""
    orm_classifier = models.Classifiers(
        project_id=project_id,
        name=classifier_create.name,
        type=classifier_type,
        archived_at=None,
    )
    session.add(orm_classifier)
    session.commit()
    session.refresh(orm_classifier)

    orm_initial_version = models.ClassifierVersions(
        classifier_id=orm_classifier.id,
        classes_dict=classifier_create.version.classes_dict,
        params=classifier_create.version.params,
    )
    session.add(orm_initial_version)
    session.commit()
    session.refresh(orm_initial_version)
    return None
