from __future__ import annotations

import time
from typing import Callable, List

from fastapi import Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app import models

rate_limit_store: dict[tuple[str, str], List[float]] = {}


def rate_limiter(limit: int, seconds: int) -> Callable:
    def dependency(request: Request) -> None:
        now = time.monotonic()
        key = (request.client.host if request.client else "anon", request.url.path)
        hits = [t for t in rate_limit_store.get(key, []) if now - t < seconds]
        if len(hits) >= limit:
            raise HTTPException(status_code=429, detail="Too Many Requests")
        hits.append(now)
        rate_limit_store[key] = hits
    return dependency


def require_api_key(x_api_key: str = Header(None), db: Session = Depends(get_db)) -> models.APIKey:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    api_key = db.query(models.APIKey).filter_by(key=x_api_key).first()
    if not api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key
