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
    classifer_response = child_crud.create_classifier(
        session=reseed_tables,
        project_id=1,
        classifier_type=base_schemas.ClassifierType.keyword_match,
        classifier_create=base_schemas.ClassifierCreate(
            name="First keyword match classifier",
            intermediatory_classes_dict={"class1": "class1 description", "class2": "class2"},
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
        "intermediatory_classes_dict": {"class1": "des", "class2": "desc"},
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
    # There is no version yet so this should be None
    # At somepoint we should return the intermediatory_classes_dict here
    assert classifier["latest_version"] is None
