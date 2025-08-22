import os
from fastapi.testclient import TestClient

os.environ.setdefault("POSTGRES_URL", "sqlite:///./test.db")

from app.main import app


def test_theme_get_put() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/themes/default")
    assert r.status_code == 200
    data = r.json()
    assert data["tokens"]["mw-green"] == "#00ff85"

    new_tokens = {"mw-green": "#123456", "mw-red": "#654321", "mw-text": "#ffffff", "mw-bg": "#000000"}
    r = client.put("/api/v1/themes/default", json={"tokens": new_tokens})
    assert r.status_code == 200

    r = client.get("/api/v1/themes/default")
    assert r.json()["tokens"]["mw-green"] == "#123456"
