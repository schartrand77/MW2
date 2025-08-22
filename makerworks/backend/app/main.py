from __future__ import annotations

from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter

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
