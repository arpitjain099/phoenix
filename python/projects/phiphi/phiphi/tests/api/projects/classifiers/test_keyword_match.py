"""Test Keyword match."""
from typing import get_args

import pytest
from fastapi.testclient import TestClient

from phiphi.api.projects.classifiers import base_schemas, child_crud, response_schemas
from phiphi.api.projects.classifiers.keyword_match import schemas as keyword_match_schemas

CREATED_TIME = "2024-04-01T12:00:01"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_keyword_match_classifier_crud(reseed_tables) -> None:
    """Test create keyword match classifier."""
    keyword_match_create = keyword_match_schemas.KeywordMatchVersionCreate(
        classes_dict={"class1": "class1 description", "class2": "class2"},
        params=keyword_match_schemas.KeywordMatchParams(
            class_to_keyword_configs=[
                keyword_match_schemas.ClassToKeywordConfig(
                    class_name="class1",
                    musts="keyword1",
                )
            ]
        ),
    )
    classifer_response = child_crud.create_classifier(
        session=reseed_tables,
        project_id=1,
        classifier_type=base_schemas.ClassifierType.keyword_match,
        classifier_create=keyword_match_schemas.KeywordMatchClassifierCreate(
            name="First keyword match classifier",
            version=keyword_match_create,
        ),
    )
    expected_types = get_args(response_schemas.AnyClassifierResponse)
    assert isinstance(classifer_response, expected_types)
    assert isinstance(classifer_response, keyword_match_schemas.KeywordMatchClassifierResponse)
    assert classifer_response.name == "First keyword match classifier"
    assert classifer_response


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_keyword_match_classifier(reseed_tables, client: TestClient) -> None:
    """Test create keyword match classifier."""
    data = {
        "name": "First keyword match classifier",
        "version": {
            "classes_dict": {"class1": "des", "class2": "desc"},
            "params": {
                "class_to_keyword_configs": [
                    {
                        "class_name": "class1",
                        "musts": "keyword1",
                    }
                ]
            },
        },
    }
    project_id = 1
    response = client.post(f"/projects/{project_id}/classifiers/keyword_match", json=data)
    assert response.status_code == 200
    classifier = response.json()

    assert classifier["name"] == data["name"]
    assert classifier["project_id"] == project_id
    assert classifier["type"] == "keyword_match"
    assert classifier["archived_at"] is None
    assert classifier["created_at"] == CREATED_TIME
    assert classifier["latest_version"]["classes_dict"] == data["version"]["classes_dict"]  # type: ignore[index]
    assert (
        classifier["latest_version"]["params"]["class_to_keyword_configs"][0]["class_name"]
        == "class1"
    )
    assert (
        classifier["latest_version"]["params"]["class_to_keyword_configs"][0]["musts"]
        == "keyword1"
    )
    assert classifier["latest_version"]["created_at"] == CREATED_TIME
