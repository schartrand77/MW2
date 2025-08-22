from __future__ import annotations

import hashlib
import hmac
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import models

router = APIRouter()


@router.post("/", response_model=dict[str, int])
def create_webhook(url: str, secret: str, db: Session = Depends(get_db)) -> dict[str, int]:
    webhook = models.Webhook(url=url, secret=secret)
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return {"id": webhook.id}


@router.post("/{webhook_id}/deliver", response_model=dict[str, str])
def deliver_webhook(webhook_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    webhook = db.get(models.Webhook, webhook_id)
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    payload = {"ping": "pong"}
    body = json.dumps(payload).encode()
    signature = hmac.new(webhook.secret.encode(), body, hashlib.sha256).hexdigest()
    log = models.WebhookDelivery(
        webhook_id=webhook.id, payload=body.decode(), signature=signature, status_code=200
    )
    db.add(log)
    db.commit()
    return {"signature": signature}
