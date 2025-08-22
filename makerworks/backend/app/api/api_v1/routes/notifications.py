from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import models
from app.api.deps import require_api_key
from app.services import notifications as notify

router = APIRouter()


@router.get("/discord", response_model=list[dict])
def discord_thread() -> list[dict]:
    return notify.fetch_discord_thread()


@router.get("/subscriptions", response_model=list[dict])
def list_subscriptions(
    api_key: models.APIKey = Depends(require_api_key),
    db: Session = Depends(get_db),
) -> list[dict]:
    subs = (
        db.query(models.NotificationSubscription)
        .filter_by(api_key_id=api_key.id)
        .all()
    )
    return [
        {
            "id": s.id,
            "event": s.event,
            "channel": s.channel,
            "target": s.target,
        }
        for s in subs
    ]


@router.post("/subscriptions", response_model=dict[str, int])
def create_subscription(
    event: str,
    channel: str,
    target: str,
    api_key: models.APIKey = Depends(require_api_key),
    db: Session = Depends(get_db),
) -> dict[str, int]:
    if channel not in {"email", "sms", "push"}:
        raise HTTPException(status_code=400, detail="invalid channel")
    sub = models.NotificationSubscription(
        api_key_id=api_key.id,
        event=event,
        channel=channel,
        target=target,
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return {"id": sub.id}


@router.post("/trigger/{event}", response_model=dict[str, int])
def trigger_event(event: str, payload: dict, db: Session = Depends(get_db)) -> dict[str, int]:
    subs = db.query(models.NotificationSubscription).filter_by(event=event).all()
    for sub in subs:
        notify.dispatch_notification(sub, payload)
    return {"sent": len(subs)}
