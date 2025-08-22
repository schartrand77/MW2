import os
from fastapi.testclient import TestClient

os.environ.setdefault("POSTGRES_URL", "sqlite:///./test.db")

from app.main import app


def test_compliance_export_delete() -> None:
    client = TestClient(app)
    api_key_resp = client.post("/api/v1/apikeys/", params={"name": "t"})
    key = api_key_resp.json()["key"]
    client.post("/api/v1/webhooks/", params={"url": "http://example.com", "secret": "s"})
    client.post(
        "/api/v1/notifications/subscriptions",
        params={"event": "e1", "channel": "email", "target": "x"},
        headers={"X-API-Key": key},
    )
    r = client.get("/api/v1/compliance/export")
    data = r.json()
    assert data["api_keys"]
    assert data["webhooks"]
    assert data["notification_subscriptions"]
    d = client.delete("/api/v1/compliance/delete")
    assert d.status_code == 200
    r2 = client.get("/api/v1/compliance/export")
    assert r2.json() == {
        "api_keys": [],
        "webhooks": [],
        "notification_subscriptions": [],
    }
