from fastapi import APIRouter

from .routes import system

api_router = APIRouter()
api_router.include_router(system.router, prefix="/system", tags=["system"])
