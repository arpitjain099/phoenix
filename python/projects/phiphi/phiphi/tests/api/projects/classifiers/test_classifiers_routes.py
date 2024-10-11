"""Test classifier routes."""
from fastapi.testclient import TestClient

from phiphi.seed.classifiers import keyword_match_seed


def test_get_classifier(reseed_tables, client: TestClient) -> None:
    """Test get classifier."""
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[0]
    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    assert response.json() == classifier.model_dump(mode="json")


def test_get_classifier_not_found(reseed_tables, client: TestClient) -> None:
    """Test get classifier not found."""
    # The seeds a keyword_match classifier in project 1
    response = client.get("/projects/2/classifiers/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Classifier not found"}

    response = client.get("/projects/1/classifiers/0")
    assert response.status_code == 404
    assert response.json() == {"detail": "Classifier not found"}


def test_get_classifiers(reseed_tables, client: TestClient) -> None:
    """Test get classifiers."""
    response = client.get("/projects/1/classifiers")
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 1
    assert json[0]["id"] == keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[0].id
    assert "intermediatory_classes" not in json[0]
