"""Test root hello world."""
from fastapi.testclient import TestClient


def test_get_root(client: TestClient) -> None:
    """Get the root hello world."""
    resp = client.get("/")
    content = resp.json()
    assert resp.status_code == 200
    assert content["message"] == "Hello World"
