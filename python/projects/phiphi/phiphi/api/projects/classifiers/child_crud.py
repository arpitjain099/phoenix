"""Child CRUD operations for the classifiers API.

At some point it might be best to integrate this into the main classifier CRUD operations.
"""
import sqlalchemy.orm

from phiphi.api.projects.classifiers import base_schemas, models, response_schemas


def create_classifier(
    session: sqlalchemy.orm.Session,
    project_id: int,
    classifier_type: base_schemas.ClassifierType,
    classifier_create: base_schemas.ClassifierCreate,
) -> response_schemas.Classifier:
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
