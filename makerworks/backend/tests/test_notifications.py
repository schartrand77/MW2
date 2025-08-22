import os

from fastapi.testclient import TestClient

os.environ.setdefault("POSTGRES_URL", "sqlite:///./test.db")

from app.main import app  # noqa: E402


def test_notification_flow() -> None:
    client = TestClient(app)
    r = client.post("/api/v1/apikeys/", params={"name": "test"})
    key = r.json()["key"]

    r2 = client.post(
        "/api/v1/notifications/subscriptions",
        headers={"X-API-Key": key},
        params={"event": "demo", "channel": "email", "target": "user@example.com"},
    )
    assert r2.status_code == 200

    r3 = client.get(
        "/api/v1/notifications/subscriptions",
        headers={"X-API-Key": key},
    )
    assert r3.status_code == 200
    assert len(r3.json()) == 1

    r4 = client.post("/api/v1/notifications/trigger/demo", json={"hello": "world"})
    assert r4.status_code == 200

    r5 = client.get("/api/v1/notifications/discord")
    assert r5.status_code == 200
    assert r5.json() == []
