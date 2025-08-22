from __future__ import annotations

import csv
import io
import json
import secrets

from fastapi import APIRouter, Depends, File, UploadFile, Response
from sqlalchemy.orm import Session

from app.db import get_db
from app import models

router = APIRouter()


@router.post("/", response_model=dict[str, str])
def create_api_key(name: str, db: Session = Depends(get_db)) -> dict[str, str]:
    key = secrets.token_hex(16)
    db_key = models.APIKey(name=name, key=key)
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    return {"key": db_key.key}


@router.get("/export", response_class=Response)
def export_api_keys(format: str = "csv", db: Session = Depends(get_db)) -> Response:
    keys = db.query(models.APIKey).all()
    if format == "json":
        data = [{"id": k.id, "name": k.name, "key": k.key} for k in keys]
        return Response(json.dumps(data), media_type="application/json")
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "name", "key"])
    writer.writeheader()
    for k in keys:
        writer.writerow({"id": k.id, "name": k.name, "key": k.key})
    return Response(output.getvalue(), media_type="text/csv")


@router.post("/import", response_model=dict[str, int])
async def import_api_keys(
    file: UploadFile = File(...),
    dry_run: bool = True,
    db: Session = Depends(get_db),
) -> dict[str, int]:
    content = (await file.read()).decode()
    reader = csv.DictReader(io.StringIO(content))
    rows = list(reader)
    if not dry_run:
        for row in rows:
            key = row.get("key") or secrets.token_hex(16)
            db.add(models.APIKey(name=row.get("name", "imported"), key=key))
        db.commit()
    return {"rows": len(rows), "dry_run": dry_run}


@router.post("/bulk-delete", response_model=dict[str, int])
def bulk_delete_api_keys(ids: list[int], db: Session = Depends(get_db)) -> dict[str, int]:
    deleted = db.query(models.APIKey).filter(models.APIKey.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    return {"deleted": deleted}
