"""Test Keyword match."""
import datetime
from typing import get_args

import freezegun
import pytest
from fastapi.testclient import TestClient

from phiphi.api.projects.classifiers import base_schemas, models, response_schemas
from phiphi.api.projects.classifiers import crud_v2 as classifier_crud
from phiphi.api.projects.classifiers.keyword_match import crud
from phiphi.api.projects.classifiers.keyword_match import schemas as keyword_match_schemas
from phiphi.seed.classifiers import keyword_match_seed

CREATED_TIME = datetime.datetime(2021, 1, 1, 0, 0, 0)
UPDATED_TIME = datetime.datetime(2021, 1, 2, 0, 0, 0)


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_keyword_match_classifier_crud(reseed_tables) -> None:
    """Test create keyword match classifier."""
    classes = [
        {
            "name": "class1",
            "description": "des",
        },
        {
            "name": "class2",
            "description": "des",
        },
    ]
    intermediatory_classes = [
        base_schemas.IntermediatoryClassCreate(
            name=class_obj["name"], description=class_obj["description"]
        )
        for class_obj in classes
    ]
    class_labels = [
        base_schemas.ClassLabel(name=class_obj["name"], description=class_obj["description"])
        for class_obj in classes
    ]
    classifer_response = classifier_crud.create_classifier(
        session=reseed_tables,
        project_id=1,
        classifier_type=base_schemas.ClassifierType.keyword_match,
        classifier_create=base_schemas.ClassifierCreate(
            name="First keyword match classifier",
            intermediatory_classes=intermediatory_classes,
        ),
    )
    expected_types = get_args(response_schemas.Classifier)
    assert isinstance(classifer_response, expected_types)
    assert isinstance(classifer_response, keyword_match_schemas.KeywordMatchClassifierResponse)
    assert classifer_response.name == "First keyword match classifier"
    assert classifer_response

    orm_classifier = reseed_tables.query(models.Classifiers).get(classifer_response.id)
    assert orm_classifier.project_id == 1
    assert orm_classifier.name == "First keyword match classifier"
    assert orm_classifier.type == "keyword_match"
    assert orm_classifier.archived_at is None
    assert orm_classifier.created_at == CREATED_TIME
    assert orm_classifier.latest_version is None

    assert orm_classifier.intermediatory_classes.count() == 2

    # Test the create of a version
    classifer_version_response = crud.create_version(
        session=reseed_tables,
        project_id=classifer_response.project_id,
        classifier_id=classifer_response.id,
    )
    assert isinstance(
        classifer_version_response, keyword_match_schemas.KeywordMatchVersionResponse
    )
    assert classifer_version_response.classifier_id == classifer_response.id
    assert classifer_version_response.classes == class_labels

    orm_classifier = classifier_crud.get_orm_classifier(reseed_tables, 1, classifer_response.id)
    assert orm_classifier.latest_version.version_id == classifer_version_response.version_id


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_keyword_match_classifier(reseed_tables, client: TestClient) -> None:
    """Test create keyword match classifier."""
    data = {
        "name": "First keyword match classifier",
        "intermediatory_classes": [
            {"name": "class1", "description": "des"},
            {"name": "class2", "description": "desc"},
        ],
    }
    project_id = 1
    response = client.post(f"/projects/{project_id}/classifiers/keyword_match", json=data)
    assert response.status_code == 200
    classifier = response.json()

    assert classifier["name"] == data["name"]
    assert classifier["project_id"] == project_id
    assert classifier["type"] == "keyword_match"
    assert classifier["archived_at"] is None
    assert classifier["created_at"] == CREATED_TIME.isoformat()
    # There is no version yet so this should be None
    assert classifier["latest_version"] is None
    assert len(classifier["intermediatory_classes"]) == 2
    assert classifier["intermediatory_classes"][0]["name"] == "class1"
    assert classifier["intermediatory_classes"][0]["description"] == "des"
    assert classifier["intermediatory_classes"][1]["name"] == "class2"


@pytest.mark.freeze_time(CREATED_TIME)
def test_patch_keyword_match_classes(reseed_tables, client: TestClient) -> None:
    """Test patch keyword match classes."""
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[0]
    patch_data = {"name": "New Name"}
    class_id = classifier.intermediatory_classes[0].id
    assert classifier.intermediatory_classes[0].name != patch_data["name"]
    with freezegun.freeze_time(UPDATED_TIME):
        response = client.patch(
            f"/projects/{classifier.project_id}/classifiers/keyword_match/{classifier.id}/intermediatory_classes/{class_id}",
            json=patch_data,
        )
    assert response.status_code == 200
    intermediate_class = response.json()
    assert intermediate_class["name"] == patch_data["name"]
    assert intermediate_class["description"] == classifier.intermediatory_classes[0].description
    assert intermediate_class["id"] == class_id
    assert intermediate_class["updated_at"] == UPDATED_TIME.isoformat()
    assert intermediate_class["created_at"] == CREATED_TIME.isoformat()

    # Get the classifier again to check the change and last_edited_at is correct
    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    json = response.json()
    assert json["last_edited_at"] == UPDATED_TIME.isoformat()
    assert json["intermediatory_classes"][0]["name"] == patch_data["name"]


@pytest.mark.freeze_time(CREATED_TIME)
def test_delete_keyword_match_classes(reseed_tables, client: TestClient) -> None:
    """Test delete keyword match classes."""
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[0]
    class_id = classifier.intermediatory_classes[0].id
    with freezegun.freeze_time(UPDATED_TIME):
        response = client.delete(
            f"/projects/{classifier.project_id}/classifiers/keyword_match/{classifier.id}/intermediatory_classes/{class_id}"
        )
    assert response.status_code == 200
    assert response.json() is None
    # Get the classifier again to check the change
    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    json = response.json()
    assert len(json["intermediatory_classes"]) == 1
    assert json["intermediatory_classes"][0]["id"] != class_id
    assert json["last_edited_at"] == UPDATED_TIME.isoformat()


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_keyword_match_intermediatory_class(reseed_tables, client: TestClient) -> None:
    """Test create keyword match intermediatory class."""
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[0]
    intermediatory_class = {
        "name": "class3",
        "description": "des3",
    }
    with freezegun.freeze_time(UPDATED_TIME):
        response = client.post(
            f"/projects/{classifier.project_id}/classifiers/keyword_match/{classifier.id}/intermediatory_classes",
            json=intermediatory_class,
        )
    assert response.status_code == 200
    version = response.json()
    assert version["created_at"] == UPDATED_TIME.isoformat()
    assert version["updated_at"] == UPDATED_TIME.isoformat()
    assert version["name"] == intermediatory_class["name"]
    assert version["description"] == intermediatory_class["description"]

    # Get the classifier again to check the change
    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    json = response.json()
    assert len(json["intermediatory_classes"]) == 3
    assert json["intermediatory_classes"][2]["name"] == intermediatory_class["name"]
    assert json["intermediatory_classes"][2]["description"] == intermediatory_class["description"]
    assert json["last_edited_at"] == UPDATED_TIME.isoformat()


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_keyword_match_intermediatory_class_non_unique_error(
    reseed_tables, client: TestClient
) -> None:
    """Test create keyword_match intermediatory_class that is not unique, should throw error."""
    # Using a classifier that has not been edited to check that `last_edited_at` is not changed on
    # error
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[3]
    intermediatory_class = {
        "name": classifier.intermediatory_classes[0].name,
        "description": "des3",
    }
    response = client.post(
        f"/projects/{classifier.project_id}/classifiers/keyword_match/{classifier.id}/intermediatory_classes",
        json=intermediatory_class,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Intermediatory Class with name already exists"}

    # Get the classifier again to check the change
    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    json = response.json()
    assert len(json["intermediatory_classes"]) == 2
    assert json["last_edited_at"] is None


@pytest.mark.freeze_time(CREATED_TIME)
def test_patch_keyword_match_intermediatory_class_non_unique_error(
    reseed_tables, client: TestClient
) -> None:
    """Test patch keyword_match intermediatory_class that is not unique, should throw error."""
    # Using a classifier that has not been edited to check that `last_edited_at` is not changed on
    # error
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[3]
    intermediatory_class = {
        "name": classifier.intermediatory_classes[1].name,
    }
    response = client.patch(
        f"/projects/{classifier.project_id}/classifiers/keyword_match/{classifier.id}/intermediatory_classes/{classifier.intermediatory_classes[0].id}",
        json=intermediatory_class,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Intermediatory Class with name already exists"}

    # Get the classifier again to check the change
    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    json = response.json()
    assert len(json["intermediatory_classes"]) == 2
    assert json["last_edited_at"] is None


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_keyword_match_intermediatory_config(reseed_tables, client: TestClient) -> None:
    """Test create keyword match intermediatory config."""
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[0]
    intermediatory_config = {
        "class_id": classifier.intermediatory_classes[0].id,
        "musts": "must1 must2",
    }
    with freezegun.freeze_time(UPDATED_TIME):
        response = client.post(
            f"/projects/{classifier.project_id}/classifiers/keyword_match/{classifier.id}/intermediatory_class_to_keyword_configs",
            json=intermediatory_config,
        )
    assert response.status_code == 200
    json = response.json()
    assert json["created_at"] == UPDATED_TIME.isoformat()
    assert json["updated_at"] == UPDATED_TIME.isoformat()
    assert json["class_id"] == intermediatory_config["class_id"]
    assert json["musts"] == intermediatory_config["musts"]
    assert json["nots"] is None
    assert json["class_name"] == classifier.intermediatory_classes[0].name

    # Get the classifier again to check the change
    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    json = response.json()
    assert json["last_edited_at"] == UPDATED_TIME.isoformat()
    assert len(json["intermediatory_class_to_keyword_configs"]) == 3
    # Due to the ordering the new config should be the second as it is order by class_id first
    assert (
        json["intermediatory_class_to_keyword_configs"][1]["class_id"]
        == intermediatory_config["class_id"]
    )
    assert (
        json["intermediatory_class_to_keyword_configs"][1]["musts"]
        == intermediatory_config["musts"]
    )


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_keyword_match_intermediatory_config_not_unique_error(
    reseed_tables, client: TestClient
) -> None:
    """Test create keyword match intermediatory config not unique."""
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[0]
    intermediatory_config = {
        "class_id": classifier.intermediatory_classes[0].id,
        "musts": "must1 must2",
    }
    with freezegun.freeze_time(UPDATED_TIME):
        response_1 = client.post(
            f"/projects/{classifier.project_id}/classifiers/keyword_match/{classifier.id}/intermediatory_class_to_keyword_configs",
            json=intermediatory_config,
        )
        response_2 = client.post(
            f"/projects/{classifier.project_id}/classifiers/keyword_match/{classifier.id}/intermediatory_class_to_keyword_configs",
            json=intermediatory_config,
        )
    assert response_1.status_code == 200
    assert response_2.status_code == 400
    assert response_2.json() == {"detail": crud.UNIQUE_ERROR_MESSAGE}
