"""Test classifier routes."""
import datetime

import pytest
from fastapi.testclient import TestClient

from phiphi.seed.classifiers import keyword_match_seed

TIMESTAMP = datetime.datetime(2021, 1, 1, 0, 0, 0)


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
    length = 2
    assert len(json) == length
    # First classifier should be last as it is id desc
    assert json[length - 1]["id"] == keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[0].id
    assert "intermediatory_classes" not in json[0]


def test_patch_classifier(reseed_tables, client: TestClient) -> None:
    """Test patch classifier."""
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[0]
    patch_data = {"name": "New Name"}
    assert classifier.name != patch_data["name"]
    response = client.patch(
        f"/projects/{classifier.project_id}/classifiers/{classifier.id}",
        json=patch_data,
    )
    assert response.status_code == 200
    assert response.json()["name"] == patch_data["name"]

    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_patch_classifier_not_found(reseed_tables, client: TestClient) -> None:
    """Test patch classifier not found."""
    response = client.patch("/projects/1/classifiers/0", json={"name": "New Name"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Classifier not found"}

    response = client.patch("/projects/2/classifiers/1", json={"name": "New Name"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Classifier not found"}

    response = client.patch("/projects/1/classifiers/2", json={"name": "New Name"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Classifier is archived."}


@pytest.mark.freeze_time(TIMESTAMP)
def test_archive_classifier(reseed_tables, client: TestClient) -> None:
    """Test archive classifier."""
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[0]
    response = client.post(
        f"/projects/{classifier.project_id}/classifiers/{classifier.id}/archive"
    )
    assert response.status_code == 200
    assert response.json()["archived_at"] == TIMESTAMP.isoformat()

    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    assert response.json()["archived_at"] == TIMESTAMP.isoformat()
