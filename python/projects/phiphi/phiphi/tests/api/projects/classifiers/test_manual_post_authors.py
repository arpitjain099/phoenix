"""Test Manual Post Authors."""
import datetime

import freezegun
import pytest
from fastapi.testclient import TestClient

from phiphi.seed.classifiers import manual_post_authors_seed

CREATED_TIME = datetime.datetime(2021, 1, 1, 0, 0, 0)
UPDATED_TIME = datetime.datetime(2021, 1, 2, 0, 0, 0)


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_manual_post_authors_classifier(reseed_tables, client: TestClient) -> None:
    """Test create keyword match classifier."""
    data = {
        "name": "First manual post authors classifier",
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
def test_create_intermediatory_classified_post_author(reseed_tables, client: TestClient) -> None:
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
                "/intermediatory_classified_post_authors/"
            ),
            json=data,
        )
    assert response.status_code == 200
    intermediatory_classified_post_author = response.json()

    assert intermediatory_classified_post_author["classifier_id"] == classifier.id
    assert intermediatory_classified_post_author["class_id"] == data["class_id"]
    assert (
        intermediatory_classified_post_author["phoenix_platform_message_author_id"]
        == data["phoenix_platform_message_author_id"]
    )
    assert intermediatory_classified_post_author["created_at"] == UPDATED_TIME.isoformat()
