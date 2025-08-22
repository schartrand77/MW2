from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_bambu_job_flow() -> None:
    r = client.post("/api/v1/printing/bambu/jobs", json={"model": "foo"})
    assert r.status_code == 200
    job_id = r.json()["id"]

    r = client.get(f"/api/v1/printing/bambu/jobs/{job_id}")
    assert r.status_code == 200
    assert r.json()["status"] == "printing"

    r = client.post("/api/v1/printing/bambu/webhook", json={"event": "done"})
    assert r.status_code == 200


def test_octoprint_job_flow() -> None:
    r = client.post("/api/v1/printing/octoprint/jobs", json={"model": "bar"})
    assert r.status_code == 200
    job_id = r.json()["id"]

    r = client.get(f"/api/v1/printing/octoprint/jobs/{job_id}")
    assert r.status_code == 200
    assert r.json()["status"] == "queued"

    r = client.post("/api/v1/printing/octoprint/webhook", json={"event": "done"})
    assert r.status_code == 200

