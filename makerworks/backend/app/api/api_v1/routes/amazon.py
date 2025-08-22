from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....db import get_db
from ....models import FeatureFlag
from ....amazon import search_items

router = APIRouter()


def require_flag(db: Session = Depends(get_db)) -> None:
    flag = db.get(FeatureFlag, "amazon_affiliate")
    if not flag or not flag.enabled:
        raise HTTPException(status_code=404)


@router.get("/search")
def amazon_search(q: str, db: Session = Depends(get_db), _: None = Depends(require_flag)) -> dict:
    items = search_items(q)
    return {"items": items}
