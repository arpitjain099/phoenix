"""Test Keyword match."""
import datetime
from typing import get_args

import pytest
from fastapi.testclient import TestClient

from phiphi.api.projects.classifiers import base_schemas, models, response_schemas
from phiphi.api.projects.classifiers import crud_v2 as classifier_crud
from phiphi.api.projects.classifiers.keyword_match import crud
from phiphi.api.projects.classifiers.keyword_match import schemas as keyword_match_schemas

CREATED_TIME = datetime.datetime(2021, 1, 1, 0, 0, 0)


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_keyword_match_classifier_crud(reseed_tables) -> None:
    """Test create keyword match classifier."""
    class_dict = {
        "class1": "des",
        "class2": "des",
    }
    intermediatory_classes = [
        base_schemas.IntermediatoryClassCreate(name=key, description=value)
        for key, value in class_dict.items()
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
    assert classifer_version_response.classes_dict == class_dict

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
