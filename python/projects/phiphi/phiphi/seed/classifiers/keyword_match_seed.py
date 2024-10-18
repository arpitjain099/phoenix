"""Classifier Keyword match seed."""
from sqlalchemy.orm import Session

from phiphi.api.projects import classifiers
from phiphi.api.projects.classifiers import base_schemas, response_schemas
from phiphi.api.projects.classifiers.keyword_match import crud, schemas

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
    name="Test keyword match Classifier 3 Versioned",
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
    name="Test keyword match Classifier 5 Versioned Failed",
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
    name="Test keyword match Classifier 6 Archived Completed",
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
    name="Test keyword match Classifier 7 Archived Failed",
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
TEST_KEYWORD_CLASSIFIER_CREATE_VERSION_RESTORE_RUNNING = base_schemas.ClassifierCreate(
    name="Test keyword match Classifier 8 Versioned Restore Running",
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
TEST_KEYWORD_CLASSIFIER_CREATE_VERSION_RESTORE_COMPLETED = base_schemas.ClassifierCreate(
    name="Test keyword match Classifier 9 Versioned Restore Completed",
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
TEST_KEYWORD_CLASSIFIER_CREATE_VERSION_RESTORE_FAILED = base_schemas.ClassifierCreate(
    name="Test keyword match Classifier 10 Versioned Restore Failed",
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

TEST_KEYWORD_CLASSIFIERS: list[response_schemas.ClassifierDetail] = []


def create_archived_classifier(
    session: Session, project_id: int, classifier_create: base_schemas.ClassifierCreate
) -> response_schemas.ClassifierDetail:
    """Create an archived classifier."""
    classifier = classifiers.crud.create_classifier(
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
    classifiers.crud.archive_classifier(
        session=session,
        project_id=project_id,
        classifier_id=classifier.id,
    )
    classifier_archived = classifiers.crud.get_classifier(
        session=session,
        project_id=project_id,
        classifier_id=classifier.id,
    )
    assert classifier_archived  # Needed for the typing
    return classifier_archived


def create_versioned_classifier(
    session: Session, project_id: int, classifier_create: base_schemas.ClassifierCreate
) -> response_schemas.ClassifierDetail:
    """Create a versioned classifier."""
    classifier = classifiers.crud.create_classifier(
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
    classifier_versioned = classifiers.crud.get_classifier(
        session=session,
        project_id=project_id,
        classifier_id=classifier.id,
    )
    assert classifier_versioned  # Needed for the typing
    return classifier_versioned


def create_test_intermediatory_class_to_keyword_config(
    session: Session,
    classifier: response_schemas.ClassifierDetail,
    class_id: int,
    musts: str,
    nots: str | None = None,
) -> None:
    """Create test intermediatory class to keyword config.

    This will update `last_edited_at` of the classifier.
    """
    intermediatory_class_to_keyword_config = schemas.IntermediatoryClassToKeywordConfigCreate(
        class_id=class_id,
        musts=musts,
        nots=nots,
    )
    crud.create_intermediatory_class_to_keyword_config(
        session=session,
        project_id=classifier.project_id,
        classifier_id=classifier.id,
        intermediatory_class_to_keyword_config=intermediatory_class_to_keyword_config,
    )


def seed_test_classifier_keyword_match(session: Session) -> None:
    """Seed test keyword match classifier."""
    # Need to clear the list before seeding other wise every seed will add to the list
    TEST_KEYWORD_CLASSIFIERS.clear()
    classifiers_to_create = [TEST_KEYWORD_CLASSIFIER_CREATE_NO_VERSION]
    project_id = 1

    for classifier_create in classifiers_to_create:
        classifier = classifiers.crud.create_classifier(
            session=session,
            project_id=project_id,
            classifier_type=base_schemas.ClassifierType.keyword_match,
            classifier_create=classifier_create,
        )
        # Create intermediatory class to keyword config
        create_test_intermediatory_class_to_keyword_config(
            session=session,
            classifier=classifier,
            class_id=classifier.intermediatory_classes[0].id,
            musts="test1",
        )
        create_test_intermediatory_class_to_keyword_config(
            session=session,
            classifier=classifier,
            class_id=classifier.intermediatory_classes[1].id,
            musts="test2",
        )
        # Need to refresh the classifier to get the most updated orm
        classifier_with_intermediatory = classifiers.crud.get_classifier(
            session=session,
            project_id=project_id,
            classifier_id=classifier.id,
        )
        assert classifier_with_intermediatory
        TEST_KEYWORD_CLASSIFIERS.append(classifier_with_intermediatory)

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

    # Job runs will be added in seed/job_runs.py
    versioned_classifiers_restored = [
        TEST_KEYWORD_CLASSIFIER_CREATE_VERSION_RESTORE_RUNNING,
        TEST_KEYWORD_CLASSIFIER_CREATE_VERSION_RESTORE_COMPLETED,
        TEST_KEYWORD_CLASSIFIER_CREATE_VERSION_RESTORE_FAILED,
    ]

    for classifier_create in versioned_classifiers_restored:
        classifier_with_version = create_versioned_classifier(
            session=session,
            project_id=project_id,
            classifier_create=classifier_create,
        )
        TEST_KEYWORD_CLASSIFIERS.append(classifier_with_version)
