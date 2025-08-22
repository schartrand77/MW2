import os
import io

from fastapi.testclient import TestClient

os.environ.setdefault("POSTGRES_URL", "sqlite:///./test.db")

from app.main import app  # noqa: E402
from app.db import SessionLocal  # noqa: E402
from app import models  # noqa: E402


def test_apikey_export_import_bulk_delete() -> None:
    client = TestClient(app)
    # create initial keys
    client.post("/api/v1/apikeys/", params={"name": "first"})
    client.post("/api/v1/apikeys/", params={"name": "second"})

    r = client.get("/api/v1/apikeys/export")
    assert r.status_code == 200
    assert "name,key" in r.text

    csv_data = "name,key\nthird,abc123\n"
    files = {"file": ("keys.csv", io.BytesIO(csv_data.encode()), "text/csv")}

    r2 = client.post("/api/v1/apikeys/import", files=files, params={"dry_run": "true"})
    assert r2.status_code == 200
    assert r2.json()["rows"] == 1

    r3 = client.post("/api/v1/apikeys/import", files=files, params={"dry_run": "false"})
    assert r3.status_code == 200
    with SessionLocal() as db:
        assert db.query(models.APIKey).filter_by(name="third").count() == 1

    with SessionLocal() as db:
        ids = [k.id for k in db.query(models.APIKey).filter(models.APIKey.name.in_(["first", "second"])).all()]
    r4 = client.post("/api/v1/apikeys/bulk-delete", json=ids)
    assert r4.status_code == 200
    with SessionLocal() as db:
        names = {k.name for k in db.query(models.APIKey).all()}
        assert "first" not in names and "second" not in names
