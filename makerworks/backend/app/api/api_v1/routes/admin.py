from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....db import get_db
from ....models import EventAudit, User
from ....security import get_current_user

router = APIRouter()


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403)
    return user


@router.get("/activity")
def activity(db: Session = Depends(get_db), user: User = Depends(require_admin)):
    events = (
        db.query(EventAudit)
        .order_by(EventAudit.created_at.desc())
        .limit(50)
        .all()
    )
    return [
        {
            "id": e.id,
            "user_id": e.user_id,
            "action": e.action,
            "data": e.data,
            "created_at": e.created_at.isoformat(),
        }
        for e in events
    ]
