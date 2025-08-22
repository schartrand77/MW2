import os
from fastapi.testclient import TestClient

os.environ.setdefault("POSTGRES_URL", "sqlite:///./test.db")

from app.main import app


def test_graphql_ping() -> None:
    client = TestClient(app)
    r = client.post("/graphql", json={"query": "{ ping }"})
    assert r.status_code == 200
    assert r.json() == {"data": {"ping": "pong"}}
