from __future__ import annotations

import json
import logging
from typing import Any, List

import httpx

from app.config import settings
from app import models

logger = logging.getLogger(__name__)


def send_email(to: str, subject: str, content: str) -> None:
    if not settings.sendgrid_api_key:
        logger.info("SendGrid not configured; skipping email to %s", to)
        return
    httpx.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {settings.sendgrid_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "personalizations": [{"to": [{"email": to}]}],
            "from": {"email": "noreply@example.com"},
            "subject": subject,
            "content": [{"type": "text/plain", "value": content}],
        },
        timeout=5,
    )


def send_sms(to: str, body: str) -> None:
    if not (
        settings.twilio_account_sid
        and settings.twilio_auth_token
        and settings.twilio_from_number
    ):
        logger.info("Twilio not configured; skipping sms to %s", to)
        return
    httpx.post(
        f"https://api.twilio.com/2010-04-01/Accounts/{settings.twilio_account_sid}/Messages.json",
        data={"To": to, "From": settings.twilio_from_number, "Body": body},
        auth=(settings.twilio_account_sid, settings.twilio_auth_token),
        timeout=5,
    )


def send_push(endpoint: str, payload: str) -> None:
    logger.info("Push to %s: %s", endpoint, payload)


def dispatch_notification(sub: models.NotificationSubscription, payload: Any) -> None:
    data = json.dumps(payload)
    if sub.channel == "email":
        send_email(sub.target, f"Event {sub.event}", data)
    elif sub.channel == "sms":
        send_sms(sub.target, data)
    elif sub.channel == "push":
        send_push(sub.target, data)


def fetch_discord_thread() -> List[dict[str, Any]]:
    token = settings.discord_bot_token
    channel_id = settings.discord_channel_id
    if not token or not channel_id:
        return []
    resp = httpx.get(
        f"https://discord.com/api/v10/channels/{channel_id}/messages",
        headers={"Authorization": f"Bot {token}"},
        timeout=5,
    )
    if resp.status_code != 200:
        return []
    return resp.json()
