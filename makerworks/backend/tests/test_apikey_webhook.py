import os
import hashlib
import hmac
import json

from fastapi.testclient import TestClient

os.environ.setdefault("POSTGRES_URL", "sqlite:///./test.db")

from app.main import app


def test_api_key_and_webhook() -> None:
    client = TestClient(app)
    r = client.post("/api/v1/apikeys/", params={"name": "test"})
    key = r.json()["key"]
    r2 = client.get("/api/v1/system/secure", headers={"X-API-Key": key})
    assert r2.status_code == 200
    assert r2.json() == {"secret": "data"}

    r3 = client.post("/api/v1/webhooks/", params={"url": "http://example.com", "secret": "abc"})
    wid = r3.json()["id"]
    r4 = client.post(f"/api/v1/webhooks/{wid}/deliver")
    sig = r4.json()["signature"]
    body = json.dumps({"ping": "pong"}).encode()
    expected = hmac.new("abc".encode(), body, hashlib.sha256).hexdigest()
    assert sig == expected
