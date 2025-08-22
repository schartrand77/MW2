from __future__ import annotations

import secrets

from fastapi import APIRouter, Depends
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
