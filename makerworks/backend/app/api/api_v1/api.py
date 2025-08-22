from fastapi import APIRouter

from .routes import system, apikeys, webhooks

api_router = APIRouter()
api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(apikeys.router, prefix="/apikeys", tags=["apikeys"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
