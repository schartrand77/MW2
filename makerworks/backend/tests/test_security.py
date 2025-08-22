import os
from fastapi.testclient import TestClient

os.environ.setdefault("POSTGRES_URL", "sqlite:///./test.db")

from app.main import app


def test_security_headers() -> None:
    client = TestClient(app)
    r = client.get("/api/v1/system/ping", headers={"origin": "http://example.com"})
    assert r.headers.get("access-control-allow-origin") == "*"
    assert "content-security-policy" in r.headers
