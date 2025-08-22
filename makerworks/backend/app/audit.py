from __future__ import annotations

from sqlalchemy.orm import Session
from datetime import datetime

from .models import EventAudit


def log_event(db: Session, user_id: str | None, action: str, data: dict | None = None) -> None:
    event = EventAudit(user_id=user_id, action=action, data=data, created_at=datetime.utcnow())
    db.add(event)
    db.commit()
