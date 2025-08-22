from __future__ import annotations

import json
import urllib.parse
from typing import Any

import httpx
from redis import Redis

from .config import settings

try:
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
except Exception:  # pragma: no cover - redis optional
    redis = None


def _cache_get(key: str) -> Any | None:
    if not redis:
        return None
    try:
        data = redis.get(key)
        return json.loads(data) if data else None
    except Exception:  # pragma: no cover - redis optional
        return None


def _cache_set(key: str, value: Any, ttl: int = 3600) -> None:
    if not redis:
        return
    try:  # pragma: no cover - redis optional
        redis.set(key, json.dumps(value), ex=ttl)
    except Exception:
        pass


def _dummy_items(query: str) -> list[dict[str, str]]:
    url = (
        f"https://www.amazon.com/s?k={urllib.parse.quote(query)}"
    )
    if settings.amazon_associate_tag:
        url += f"&tag={settings.amazon_associate_tag}"
    return [{"title": f"Sample result for {query}", "url": url}]


def search_items(query: str) -> list[dict[str, str]]:
    cache_key = f"amazon:{query}"
    cached = _cache_get(cache_key)
    if cached:
        return cached
    if not (
        settings.amazon_paapi_access_key
        and settings.amazon_paapi_secret_key
        and settings.amazon_associate_tag
    ):
        items = _dummy_items(query)
    else:  # pragma: no cover - external API
        # Real PA-API request would go here
        params = {
            "Keywords": query,
            "PartnerTag": settings.amazon_associate_tag,
            "PartnerType": "Associates",
        }
        with httpx.Client() as client:
            client.get("https://example.com", params=params)  # placeholder
        items = _dummy_items(query)
    _cache_set(cache_key, items)
    return items
