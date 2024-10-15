"""Test classifier routes."""
import datetime
from unittest import mock

import pytest
from fastapi.testclient import TestClient
from prefect.client.schemas import objects

from phiphi.api.projects.job_runs import schemas as job_run_schemas
from phiphi.seed.classifiers import keyword_match_seed

TIMESTAMP = datetime.datetime(2021, 1, 1, 0, 0, 0)


def test_get_classifier(reseed_tables, client: TestClient) -> None:
    """Test get classifier."""
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[0]
    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    json = response.json()
    assert json == classifier.model_dump(mode="json")
    assert "latest_version" in json
    assert json["latest_version"] is None
    assert "latest_job_run" in json
    assert json["latest_job_run"] is None
    assert "intermediatory_classes" in json


def test_get_classifier_not_found(reseed_tables, client: TestClient) -> None:
    """Test get classifier not found."""
    # The seeds a keyword_match classifier in project 1
    response = client.get("/projects/2/classifiers/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Classifier not found"}

    response = client.get("/projects/1/classifiers/0")
    assert response.status_code == 404
    assert response.json() == {"detail": "Classifier not found"}


def test_get_classifier_with_version_and_job(reseed_tables, client: TestClient) -> None:
    """Test get classifier."""
    # Classifier with a version
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[2]
    assert classifier.latest_version
    assert classifier.latest_job_run
    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    json = response.json()
    assert json == classifier.model_dump(mode="json")
    assert "latest_version" in json
    assert json["latest_version"]["version_id"] == classifier.latest_version.version_id
    assert "latest_job_run" in json
    assert json["latest_job_run"]["id"] == classifier.latest_job_run.id


def test_get_classifiers(reseed_tables, client: TestClient) -> None:
    """Test get classifiers."""
    # Doing start and end so we don't have to worry about the number of classifiers
    # in the seeds
    response = client.get("/projects/1/classifiers?start=0&end=4")
    assert response.status_code == 200
    json = response.json()
    length = 4
    assert len(json) == length
    # Desc order
    assert json[length - 1]["id"] < json[0]["id"]
    assert "intermediatory_classes" not in json[0]
    assert "latest_job_run" in json[0]


@pytest.mark.freeze_time(TIMESTAMP)
def test_patch_classifier(reseed_tables, client: TestClient) -> None:
    """Test patch classifier."""
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[0]
    patch_data = {"name": "New Name"}
    assert classifier.name != patch_data["name"]
    assert classifier.last_edited_at is None
    response = client.patch(
        f"/projects/{classifier.project_id}/classifiers/{classifier.id}",
        json=patch_data,
    )
    assert response.status_code == 200
    assert response.json()["name"] == patch_data["name"]
    assert response.json()["last_edited_at"] == TIMESTAMP.isoformat()

    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"
    assert response.json()["last_edited_at"] == TIMESTAMP.isoformat()


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
@mock.patch("phiphi.api.projects.job_runs.prefect_deployment.wrapped_run_deployment")
def test_archive_classifier(m_run_deployment, reseed_tables, client: TestClient) -> None:
    """Test archive classifier."""
    mock_flow_run = mock.MagicMock(spec=objects.FlowRun)
    mock_flow_run.id = "mock_uuid"
    mock_flow_run.name = "mock_flow_run"
    m_run_deployment.return_value = mock_flow_run
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[0]
    response = client.post(
        f"/projects/{classifier.project_id}/classifiers/{classifier.id}/archive"
    )
    m_run_deployment.assert_called_once_with(
        name="flow_runner_flow/flow_runner_flow",
        parameters={
            "project_id": classifier.project_id,
            "job_type": job_run_schemas.ForeignJobType.classifier_archive,
            "job_source_id": classifier.id,
            "job_run_id": mock.ANY,
        },
    )
    assert response.status_code == 200
    assert response.json()["archived_at"] == TIMESTAMP.isoformat()

    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    assert response.json()["archived_at"] == TIMESTAMP.isoformat()


@pytest.mark.freeze_time(TIMESTAMP)
@mock.patch("phiphi.api.projects.job_runs.prefect_deployment.wrapped_run_deployment")
def test_restore_classifier(m_run_deployment, reseed_tables, client: TestClient) -> None:
    """Test restore classifier."""
    mock_flow_run = mock.MagicMock(spec=objects.FlowRun)
    mock_flow_run.id = "mock_uuid"
    mock_flow_run.name = "mock_flow_run"
    m_run_deployment.return_value = mock_flow_run
    # Classifier 1 is archived
    classifier = keyword_match_seed.TEST_KEYWORD_CLASSIFIERS[1]
    assert classifier.archived_at is not None
    response = client.post(
        f"/projects/{classifier.project_id}/classifiers/{classifier.id}/restore"
    )
    m_run_deployment.assert_called_once_with(
        name="flow_runner_flow/flow_runner_flow",
        parameters={
            "project_id": classifier.project_id,
            "job_type": job_run_schemas.ForeignJobType.classifier_restore,
            "job_source_id": classifier.id,
            "job_run_id": mock.ANY,
        },
    )
    assert response.status_code == 200
    assert response.json()["archived_at"] is None

    response = client.get(f"/projects/{classifier.project_id}/classifiers/{classifier.id}")
    assert response.status_code == 200
    assert response.json()["archived_at"] is None
