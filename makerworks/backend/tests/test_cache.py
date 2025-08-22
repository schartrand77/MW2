import os
from fastapi.testclient import TestClient


def test_etag(monkeypatch):
    monkeypatch.setenv("POSTGRES_URL", "sqlite:///./test.db")
    from app.main import create_app

    app = create_app()
    client = TestClient(app)
    r1 = client.get("/api/v1/system/ping")
    assert r1.status_code == 200
    etag = r1.headers.get("etag")
    assert etag
    r2 = client.get("/api/v1/system/ping", headers={"If-None-Match": etag})
    assert r2.status_code == 304
