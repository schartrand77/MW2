from fastapi.testclient import TestClient

from app.main import app


def test_ping() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/system/ping")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
