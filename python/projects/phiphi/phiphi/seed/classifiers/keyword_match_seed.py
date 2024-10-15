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
    name="Test keyword match Classifier 2 Running Archived",
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

# Needed for the console development
TEST_KEYWORD_CLASSIFIER_CREATE_VERSION_COMPLETED = base_schemas.ClassifierCreate(
    name="Test keyword match Classifier 4 Versioned Completed",
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

# Needed for the console development
TEST_KEYWORD_CLASSIFIER_CREATE_VERSION_FAILED = base_schemas.ClassifierCreate(
    name="Test keyword match Classifier 4 Versioned Failed",
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

# Needed for the console development
TEST_KEYWORD_CLASSIFIER_COMPLETED_ARCHIVED = base_schemas.ClassifierCreate(
    name="Test keyword match Classifier 2 Archived Completed",
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

# Needed for the console development
TEST_KEYWORD_CLASSIFIER_FAILED_ARCHIVED = base_schemas.ClassifierCreate(
    name="Test keyword match Classifier 2 Archived Failed",
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


def create_archived_classifier(
    session: Session, project_id: int, classifier_create: base_schemas.ClassifierCreate
) -> response_schemas.Classifier:
    """Create an archived classifier."""
    classifier = classifier_crud.create_classifier(
        session=session,
        project_id=project_id,
        classifier_type=base_schemas.ClassifierType.keyword_match,
        classifier_create=classifier_create,
    )
    classifier_crud.archive_classifier(
        session=session,
        project_id=project_id,
        classifier_id=classifier.id,
    )
    classifier_archived = classifier_crud.get_classifier(
        session=session,
        project_id=project_id,
        classifier_id=classifier.id,
    )
    assert classifier_archived  # Needed for the typing
    return classifier_archived


def create_versioned_classifier(
    session: Session, project_id: int, classifier_create: base_schemas.ClassifierCreate
) -> response_schemas.Classifier:
    """Create a versioned classifier."""
    classifier = classifier_crud.create_classifier(
        session=session,
        project_id=project_id,
        classifier_type=base_schemas.ClassifierType.keyword_match,
        classifier_create=classifier_create,
    )
    crud.create_version(
        session=session,
        project_id=project_id,
        classifier_id=classifier.id,
    )
    # Need to refresh the classifier to get the latest version
    classifier_versioned = classifier_crud.get_classifier(
        session=session,
        project_id=project_id,
        classifier_id=classifier.id,
    )
    assert classifier_versioned  # Needed for the typing
    return classifier_versioned


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

    archived_classifier = create_archived_classifier(
        session=session,
        project_id=project_id,
        classifier_create=TEST_KEYWORD_CLASSIFIER_CREATE_ARCHIVED,
    )
    TEST_KEYWORD_CLASSIFIERS.append(archived_classifier)

    versioned_classifiers = [
        TEST_KEYWORD_CLASSIFIER_CREATE_VERSIONED,
        TEST_KEYWORD_CLASSIFIER_CREATE_VERSION_COMPLETED,
        TEST_KEYWORD_CLASSIFIER_CREATE_VERSION_FAILED,
    ]

    for classifier_create in versioned_classifiers:
        classifier_with_version = create_versioned_classifier(
            session=session,
            project_id=project_id,
            classifier_create=classifier_create,
        )
        TEST_KEYWORD_CLASSIFIERS.append(classifier_with_version)

    archived_classifiers = [
        TEST_KEYWORD_CLASSIFIER_COMPLETED_ARCHIVED,
        TEST_KEYWORD_CLASSIFIER_FAILED_ARCHIVED,
    ]
    for classifier_create in archived_classifiers:
        archived_classifier = create_archived_classifier(
            session=session,
            project_id=project_id,
            classifier_create=classifier_create,
        )
        TEST_KEYWORD_CLASSIFIERS.append(archived_classifier)
