"""Classifier Manual Post Authors seed."""
from sqlalchemy.orm import Session

from phiphi.api.projects import classifiers
from phiphi.api.projects.classifiers import base_schemas
from phiphi.api.projects.classifiers.manual_post_authors import crud, schemas

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

TEST_MANUAL_POST_AUTHORS_CREATE_NO_VERSION_CLASSIFIED = base_schemas.ClassifierCreate(
    name="Test keyword match Classifier 1 no version with intermediatory classified post authors",
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

TEST_MANUAL_POST_AUTHORS_CLASSIFIERS: list[schemas.ManualPostAuthorsClassifierDetail] = []


def create_intermediatory_classified_post_authors(
    session: Session,
    classifier: schemas.ManualPostAuthorsClassifierDetail,
    intermediatory_classified_post_authors_create: list[schemas.IntermediatoryAuthorClassCreate],
) -> schemas.ManualPostAuthorsClassifierDetail:
    """Create intermediatory classified post authors."""
    for create_obj in intermediatory_classified_post_authors_create:
        _ = crud.create_intermediatory_classified_post_authors(
            session=session,
            project_id=classifier.project_id,
            classifier_id=classifier.id,
            create_obj=create_obj,
        )

    # Refresh classifier
    classifier_with_intermediatory = classifiers.crud.get_classifier(
        session, classifier.project_id, classifier.id
    )
    # Needed for mypy
    assert isinstance(classifier_with_intermediatory, schemas.ManualPostAuthorsClassifierDetail)
    return classifier_with_intermediatory


def seed_test_classifiers_manual_post_authors(session: Session) -> None:
    """Seed test classifiers."""
    TEST_MANUAL_POST_AUTHORS_CLASSIFIERS.clear()
    project_id = 2

    classifiers_create = [
        TEST_MANUAL_POST_AUTHORS_CREATE_NO_VERSION,
        TEST_MANUAL_POST_AUTHORS_CREATE_NO_VERSION_CLASSIFIED,
    ]

    for classifier_create in classifiers_create:
        classifier = classifiers.crud.create_classifier(
            session=session,
            project_id=project_id,
            classifier_type=base_schemas.ClassifierType.manual_post_authors,
            classifier_create=classifier_create,
        )
        assert isinstance(classifier, schemas.ManualPostAuthorsClassifierDetail)
        TEST_MANUAL_POST_AUTHORS_CLASSIFIERS.append(classifier)

    classifier_to_create_intermediatory = TEST_MANUAL_POST_AUTHORS_CLASSIFIERS[1]
    TEST_MANUAL_POST_AUTHORS_CLASSIFIERS[1] = create_intermediatory_classified_post_authors(
        session=session,
        classifier=classifier_to_create_intermediatory,
        intermediatory_classified_post_authors_create=[
            schemas.IntermediatoryAuthorClassCreate(
                class_id=classifier_to_create_intermediatory.intermediatory_classes[0].id,
                phoenix_platform_message_author_id="author1",
            )
        ],
    )
