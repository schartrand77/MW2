import os
from fastapi.testclient import TestClient

os.environ.setdefault("POSTGRES_URL", "sqlite:///./test.db")

from app.main import app


def test_rate_limit() -> None:
    client = TestClient(app)
    url = "/api/v1/system/limited"
    assert client.get(url).status_code == 200
    assert client.get(url).status_code == 200
    r = client.get(url)
    assert r.status_code == 429
