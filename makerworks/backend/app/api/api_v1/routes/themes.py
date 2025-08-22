from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import models

router = APIRouter()

DEFAULT_TOKENS = {
    "mw-green": "#00ff85",
    "mw-red": "#ff0040",
    "mw-text": "#ffffff",
    "mw-bg": "#1b1b1b",
}


@router.get("/{org}")
def get_theme(org: str, db: Session = Depends(get_db)):
    theme = db.query(models.Theme).filter_by(org=org).first()
    if not theme:
        return {"org": org, "tokens": DEFAULT_TOKENS}
    return {"org": org, "tokens": theme.tokens}


@router.put("/{org}")
def put_theme(org: str, payload: dict, db: Session = Depends(get_db)):
    tokens = payload.get("tokens")
    if not isinstance(tokens, dict):
        raise HTTPException(status_code=400, detail="Invalid tokens")
    theme = db.query(models.Theme).filter_by(org=org).first()
    if not theme:
        theme = models.Theme(org=org, tokens=tokens)
        db.add(theme)
    else:
        theme.tokens = tokens
    db.commit()
    return {"status": "ok"}
