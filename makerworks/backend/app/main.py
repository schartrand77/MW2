from __future__ import annotations

import hashlib

from fastapi import FastAPI, Request, Response
import strawberry
from strawberry.fastapi import GraphQLRouter
from prometheus_client import Counter, make_asgi_app

from .api.api_v1.api import api_router
from .config import settings
from .plugins import load_plugins


@strawberry.type
class Query:
    @strawberry.field
    def ping(self) -> str:
        return "pong"


schema = strawberry.Schema(query=Query)

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "path"]
)


def create_app() -> FastAPI:
    app = FastAPI(title="MakerWorks API")
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(GraphQLRouter(schema), prefix="/graphql")

    @app.middleware("http")
    async def count_requests(request: Request, call_next):
        response = await call_next(request)
        REQUEST_COUNT.labels(request.method, request.url.path).inc()
        return response

    @app.middleware("http")
    async def cache_headers(request: Request, call_next):
        response: Response = await call_next(request)
        if response.status_code != 200 or request.url.path.startswith("/metrics"):
            return response

        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        etag = hashlib.sha1(body).hexdigest()
        if request.headers.get("if-none-match") == etag:
            return Response(status_code=304)
        headers = dict(response.headers)
        headers.setdefault(
            "Cache-Control", "public, max-age=60, stale-while-revalidate=30"
        )
        headers.setdefault("Content-Type", response.headers.get("Content-Type", "application/json"))
        headers["ETag"] = etag
        return Response(content=body, status_code=response.status_code, headers=headers, media_type=response.media_type)

    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    load_plugins(app, settings.plugins)

    return app


app = create_app()
