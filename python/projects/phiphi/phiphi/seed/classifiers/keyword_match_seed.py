"""Classifier Keyword match seed."""
from sqlalchemy.orm import Session

from phiphi.api.projects.classifiers import base_schemas, response_schemas
from phiphi.api.projects.classifiers import crud_v2 as classifier_crud
from phiphi.api.projects.classifiers.keyword_match import crud

TEST_KEYWORD_CLASSIFIER_CREATE_NO_VERSION = base_schemas.ClassifierCreate(
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

TEST_KEYWORD_CLASSIFIER_CREATE_ARCHIVED = base_schemas.ClassifierCreate(
    name="Test keyword match Classifier 2 Archived",
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

TEST_KEYWORD_CLASSIFIER_CREATE_VERSIONED = base_schemas.ClassifierCreate(
    name="Test keyword match Classifier 2 Versioned",
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
    classifiers = [TEST_KEYWORD_CLASSIFIER_CREATE_NO_VERSION]
    project_id = 1

    for classifier_create in classifiers:
        classifier = classifier_crud.create_classifier(
            session=session,
            project_id=project_id,
            classifier_type=base_schemas.ClassifierType.keyword_match,
            classifier_create=classifier_create,
        )
        TEST_KEYWORD_CLASSIFIERS.append(classifier)

    classifier = classifier_crud.create_classifier(
        session=session,
        project_id=project_id,
        classifier_type=base_schemas.ClassifierType.keyword_match,
        classifier_create=TEST_KEYWORD_CLASSIFIER_CREATE_ARCHIVED,
    )
    archived_classifier = classifier_crud.archive_classifier(
        session=session,
        project_id=project_id,
        classifier_id=classifier.id,
    )
    # Need to check for typing errors
    assert archived_classifier
    TEST_KEYWORD_CLASSIFIERS.append(archived_classifier)

    classifier = classifier_crud.create_classifier(
        session=session,
        project_id=project_id,
        classifier_type=base_schemas.ClassifierType.keyword_match,
        classifier_create=TEST_KEYWORD_CLASSIFIER_CREATE_VERSIONED,
    )
    _ = crud.create_version(
        session=session,
        project_id=project_id,
        classifier_id=classifier.id,
    )
    # Need to refresh the classifier so the response includes latest version
    classifier_with_version = classifier_crud.get_classifier(
        session=session,
        project_id=project_id,
        classifier_id=classifier.id,
    )
    # Needed for the typing
    assert classifier_with_version
    TEST_KEYWORD_CLASSIFIERS.append(classifier_with_version)
