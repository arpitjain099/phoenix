"""Test Manual Post Authors."""
import datetime

import freezegun
import pytest
from fastapi.testclient import TestClient

from phiphi.api.projects.classifiers.manual_post_authors import crud
from phiphi.seed.classifiers import manual_post_authors_seed

CREATED_TIME = datetime.datetime(2021, 1, 1, 0, 0, 0)
UPDATED_TIME = datetime.datetime(2021, 1, 2, 0, 0, 0)


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_manaual_post_authors_version(reseed_tables, client: TestClient, session) -> None:
    """Test create manual post authors version."""
    classifier = manual_post_authors_seed.TEST_MANUAL_POST_AUTHORS_CLASSIFIERS[1]
    project_id = classifier.project_id
    classifier_id = classifier.id

    version = crud.create_version(session, project_id, classifier_id)

    assert version.classifier_id == classifier_id
    assert len(version.classes) == 2
    assert version.classes[0].name == classifier.intermediatory_classes[0].name
    assert version.classes[1].name == classifier.intermediatory_classes[1].name
    expected_author_classes = classifier.intermediatory_author_classes
    assert len(version.params["author_classes"]) == len(expected_author_classes)
    for i, author_class in enumerate(version.params["author_classes"]):
        assert author_class["class_name"] == expected_author_classes[i].class_name
        assert (
            author_class["phoenix_platform_message_author_id"]
            == expected_author_classes[i].phoenix_platform_message_author_id
        )


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_manual_post_authors_classifier(reseed_tables, client: TestClient) -> None:
    """Test create keyword match classifier."""
    data = {
        "name": "First manual post authors classifier",
        "description": "First manual post authors classifier description",
        "intermediatory_classes": [
            {"name": "class1", "description": "des"},
            {"name": "class2", "description": "desc"},
        ],
    }
    project_id = 1
    response = client.post(f"/projects/{project_id}/classifiers/manual_post_authors", json=data)
    assert response.status_code == 200
    classifier = response.json()

    assert classifier["name"] == data["name"]
    assert classifier["project_id"] == project_id
    assert classifier["type"] == "manual_post_authors"
    assert classifier["archived_at"] is None
    assert classifier["created_at"] == CREATED_TIME.isoformat()
    # There is no version yet so this should be None
    assert classifier["latest_version"] is None
    assert len(classifier["intermediatory_classes"]) == 2
    assert classifier["intermediatory_classes"][0]["name"] == "class1"
    assert classifier["intermediatory_classes"][0]["description"] == "des"
    assert classifier["intermediatory_classes"][1]["name"] == "class2"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_intermediatory_author_class(reseed_tables, client: TestClient) -> None:
    """Test create intermediatory classified post author."""
    classifier = manual_post_authors_seed.TEST_MANUAL_POST_AUTHORS_CLASSIFIERS[0]
    project_id = classifier.project_id
    author_id = "author1"
    data = {
        "class_id": classifier.intermediatory_classes[0].id,
        "phoenix_platform_message_author_id": author_id,
    }
    with freezegun.freeze_time(UPDATED_TIME):
        response = client.post(
            (
                f"/projects/{project_id}"
                f"/classifiers/manual_post_authors/{classifier.id}"
                "/intermediatory_author_classes/"
            ),
            json=data,
        )
    assert response.status_code == 200
    intermediatory_author_class = response.json()

    assert intermediatory_author_class["classifier_id"] == classifier.id
    assert intermediatory_author_class["class_id"] == data["class_id"]
    assert (
        intermediatory_author_class["phoenix_platform_message_author_id"]
        == data["phoenix_platform_message_author_id"]
    )
    assert intermediatory_author_class["created_at"] == UPDATED_TIME.isoformat()
    assert intermediatory_author_class["class_name"] == classifier.intermediatory_classes[0].name

    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    json = response.json()
    assert json["last_edited_at"] == UPDATED_TIME.isoformat()
    assert len(json["intermediatory_author_classes"]) == 1
    assert json["intermediatory_author_classes"][0] == intermediatory_author_class


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_intermediatory_author_class_non_unique_error(
    reseed_tables, client: TestClient
) -> None:
    """Test create intermediatory classified post author not unique."""
    classifier = manual_post_authors_seed.TEST_MANUAL_POST_AUTHORS_CLASSIFIERS[1]
    project_id = classifier.project_id
    duplicated_obj = classifier.intermediatory_author_classes[0]
    data = {
        "class_id": duplicated_obj.class_id,
        "phoenix_platform_message_author_id": duplicated_obj.phoenix_platform_message_author_id,
    }
    with freezegun.freeze_time(UPDATED_TIME):
        response = client.post(
            (
                f"/projects/{project_id}"
                f"/classifiers/manual_post_authors/{classifier.id}"
                "/intermediatory_author_classes/"
            ),
            json=data,
        )

    assert response.status_code == 400
    assert response.json() == {"detail": crud.UNIQUE_ERROR_MESSAGE}


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_intermediatory_author_class_class_not_found(
    reseed_tables, client: TestClient
) -> None:
    """Test create intermediatory classified post author class not found."""
    classifier = manual_post_authors_seed.TEST_MANUAL_POST_AUTHORS_CLASSIFIERS[1]
    project_id = classifier.project_id
    author_id = classifier.intermediatory_author_classes[0].phoenix_platform_message_author_id
    data = {
        "class_id": 0,
        "phoenix_platform_message_author_id": author_id,
    }
    with freezegun.freeze_time(UPDATED_TIME):
        response = client.post(
            (
                f"/projects/{project_id}"
                f"/classifiers/manual_post_authors/{classifier.id}"
                "/intermediatory_author_classes/"
            ),
            json=data,
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "Intermediatory Class not found"}


@pytest.mark.freeze_time(CREATED_TIME)
def test_delete_intermediatory_author_class(reseed_tables, client: TestClient) -> None:
    """Test delete intermediatory classified post author."""
    classifier = manual_post_authors_seed.TEST_MANUAL_POST_AUTHORS_CLASSIFIERS[1]
    project_id = classifier.project_id
    obj_id = classifier.intermediatory_author_classes[0].id

    with freezegun.freeze_time(UPDATED_TIME):
        response = client.delete(
            (
                f"/projects/{project_id}"
                f"/classifiers/manual_post_authors/{classifier.id}"
                f"/intermediatory_author_classes/{obj_id}"
            )
        )
    assert response.status_code == 200
    assert response.json() is None

    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    json = response.json()
    assert json["last_edited_at"] == UPDATED_TIME.isoformat()
    assert len(json["intermediatory_author_classes"]) == 2


@pytest.mark.freeze_time(CREATED_TIME)
def test_patch_manual_post_authors_classes(reseed_tables, client: TestClient) -> None:
    """Test patch manual post authors classes."""
    classifier = manual_post_authors_seed.TEST_MANUAL_POST_AUTHORS_CLASSIFIERS[1]
    project_id = classifier.project_id
    class_id = classifier.intermediatory_classes[0].id
    data = {"name": "new_name", "description": "new_desc"}

    with freezegun.freeze_time(UPDATED_TIME):
        response = client.patch(
            (
                f"/projects/{project_id}"
                f"/classifiers/{classifier.id}"
                f"/intermediatory_classes/{class_id}"
            ),
            json=data,
        )
    assert response.status_code == 200
    updated_class = response.json()

    assert updated_class["id"] == class_id
    assert updated_class["name"] == data["name"]
    assert updated_class["description"] == data["description"]

    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    json = response.json()
    assert json["last_edited_at"] == UPDATED_TIME.isoformat()
    assert len(json["intermediatory_classes"]) == 2
    assert json["intermediatory_classes"][0] == updated_class
    # Important to check that the intermediatory_author_classes class name is now updated
    assert json["intermediatory_author_classes"][0]["class_name"] == data["name"]


@pytest.mark.freeze_time(CREATED_TIME)
def test_deleted_manual_post_authors_classes(reseed_tables, client: TestClient) -> None:
    """Test delete manual post authors classes."""
    classifier = manual_post_authors_seed.TEST_MANUAL_POST_AUTHORS_CLASSIFIERS[1]
    project_id = classifier.project_id
    class_id = classifier.intermediatory_classes[0].id

    with freezegun.freeze_time(UPDATED_TIME):
        response = client.delete(
            (
                f"/projects/{project_id}"
                f"/classifiers/{classifier.id}"
                f"/intermediatory_classes/{class_id}"
            )
        )
    assert response.status_code == 200
    assert response.json() is None

    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    json = response.json()
    assert json["last_edited_at"] == UPDATED_TIME.isoformat()
    assert len(json["intermediatory_classes"]) == 1
    assert json["intermediatory_classes"][0]["id"] == classifier.intermediatory_classes[1].id
    # There is one class with id 2 in the intermediatory_author_classes
    assert len(json["intermediatory_author_classes"]) == 1


@pytest.mark.patch_settings({"USE_MOCK_BQ": True})
@pytest.mark.freeze_time(CREATED_TIME)
def test_manual_post_authors_get_post_authors_with_mock_bq(
    patch_settings,
    reseed_tables,
    client: TestClient,
    pipeline_jobs_sample_generalised_post_authors,
) -> None:
    """Test get post authors when USE_MOCK_BQ is enabled."""
    classifier = manual_post_authors_seed.TEST_MANUAL_POST_AUTHORS_CLASSIFIERS[1]
    class_1 = classifier.intermediatory_classes[0].name
    class_2 = classifier.intermediatory_classes[1].name
    response = client.get(
        f"/projects/{classifier.project_id}/classifiers/manual_post_authors/{classifier.id}/authors/"
    )
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 10
    assert json[0]["phoenix_platform_message_author_id"] == "id_1"
    assert len(json[0]["intermediatory_author_classes"]) == 2
    assert json[0]["intermediatory_author_classes"][0]["class_name"] == class_1
    assert json[0]["intermediatory_author_classes"][1]["class_name"] == class_2
    assert json[1]["phoenix_platform_message_author_id"] == "id_2"
    assert len(json[1]["intermediatory_author_classes"]) == 0
    assert len(json[2]["intermediatory_author_classes"]) == 1
    assert json[2]["intermediatory_author_classes"][0]["class_name"] == class_1
    expected_df = pipeline_jobs_sample_generalised_post_authors[:10]
    assert (
        json[0]["phoenix_platform_message_author_id"]
        == expected_df.iloc[0]["phoenix_platform_message_author_id"]
    )
    assert (
        json[9]["phoenix_platform_message_author_id"]
        == expected_df.iloc[9]["phoenix_platform_message_author_id"]
    )
