from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app import models

router = APIRouter()


@router.get("/export", response_model=dict)
def export_data(db: Session = Depends(get_db)) -> dict:
    api_keys = [
        {"id": k.id, "name": k.name, "key": k.key}
        for k in db.query(models.APIKey).all()
    ]
    webhooks = [
        {"id": w.id, "url": w.url, "secret": w.secret}
        for w in db.query(models.Webhook).all()
    ]
    subs = [
        {
            "id": s.id,
            "event": s.event,
            "channel": s.channel,
            "target": s.target,
        }
        for s in db.query(models.NotificationSubscription).all()
    ]
    return {
        "api_keys": api_keys,
        "webhooks": webhooks,
        "notification_subscriptions": subs,
    }


@router.delete("/delete", response_model=dict)
def delete_data(db: Session = Depends(get_db)) -> dict:
    counts = {
        "api_keys": db.query(models.APIKey).delete(),
        "webhooks": db.query(models.Webhook).delete(),
        "notification_subscriptions": db.query(models.NotificationSubscription).delete(),
    }
    db.commit()
    return counts


@router.get("/checklist", response_model=dict)
def compliance_checklist() -> dict:
    return {
        "items": [
            "Data retention policy",
            "Encryption at rest",
            "User consent management",
            "Right to be forgotten",
        ]
    }
