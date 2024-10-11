"""Classifier Keyword match seed."""
from sqlalchemy.orm import Session

from phiphi.api.projects.classifiers import base_schemas, response_schemas
from phiphi.api.projects.classifiers import crud_v2 as crud

TEST_KEYWORD_CLASSIFIER_CREATE_1 = base_schemas.ClassifierCreate(
    name="Test keyword match Classifier 1",
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

TEST_KEYWORD_CLASSIFIER_CREATE_2 = base_schemas.ClassifierCreate(
    name="Test keyword match Classifier 2 Archieved",
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

TEST_KEYWORD_CLASSIFIERS: list[response_schemas.Classifier] = []


def seed_test_classifier_keyword_match(session: Session) -> None:
    """Seed test keyword match classifier."""
    # Need to clear the list before seeding other wise every seed will add to the list
    TEST_KEYWORD_CLASSIFIERS.clear()
    classifiers = [
        TEST_KEYWORD_CLASSIFIER_CREATE_1,
    ]

    for classifier_create in classifiers:
        classifier = crud.create_classifier(
            session=session,
            project_id=1,
            classifier_type=base_schemas.ClassifierType.keyword_match,
            classifier_create=classifier_create,
        )
        TEST_KEYWORD_CLASSIFIERS.append(classifier)

    classifier = crud.create_classifier(
        session=session,
        project_id=1,
        classifier_type=base_schemas.ClassifierType.keyword_match,
        classifier_create=TEST_KEYWORD_CLASSIFIER_CREATE_2,
    )
    archived_classifier = crud.archive_classifier(
        session=session,
        project_id=1,
        classifier_id=classifier.id,
    )
    # Need to check for typing errors
    assert archived_classifier
    TEST_KEYWORD_CLASSIFIERS.append(archived_classifier)
