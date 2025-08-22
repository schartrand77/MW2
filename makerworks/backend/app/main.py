from __future__ import annotations

from fastapi import FastAPI, Request
import strawberry
from strawberry.fastapi import GraphQLRouter
from prometheus_client import Counter, make_asgi_app

from .api.api_v1.api import api_router


@strawberry.type
class Query:
    @strawberry.field
    def ping(self) -> str:
        return "pong"


schema = strawberry.Schema(query=Query)

app = FastAPI(title="MakerWorks API")
app.include_router(api_router, prefix="/api/v1")
app.include_router(GraphQLRouter(schema), prefix="/graphql")

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "path"]
)


@app.middleware("http")
async def count_requests(request: Request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(request.method, request.url.path).inc()
    return response


metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
