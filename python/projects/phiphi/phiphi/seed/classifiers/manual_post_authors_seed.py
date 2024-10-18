"""Classifier Manual Post Authors seed."""
from sqlalchemy.orm import Session

from phiphi.api.projects import classifiers
from phiphi.api.projects.classifiers import base_schemas, response_schemas

TEST_MANUAL_POST_AUTHORS_CREATE_NO_VERSION = base_schemas.ClassifierCreate(
    name="Test keyword match Classifier 1 no version",
    intermediatory_classes=[
        base_schemas.IntermediatoryClassCreate(
            name="Test Class 1",
            description="Test Class 1 Description",
        ),
        base_schemas.IntermediatoryClassCreate(
            name="Test Class 2",
            description="Test Class 2 Description",
        ),
    ],
)

TEST_MANUAL_POST_AUTHORS_CLASSIFIERS: list[response_schemas.ClassifierDetail] = []


def seed_test_classifiers_manual_post_authors(session: Session) -> None:
    """Seed test classifiers."""
    TEST_MANUAL_POST_AUTHORS_CLASSIFIERS.clear()
    project_id = 2
    classifier = classifiers.crud.create_classifier(
        session=session,
        project_id=project_id,
        classifier_type=base_schemas.ClassifierType.manual_post_authors,
        classifier_create=TEST_MANUAL_POST_AUTHORS_CREATE_NO_VERSION,
    )
    TEST_MANUAL_POST_AUTHORS_CLASSIFIERS.append(classifier)
