from fastapi import APIRouter

from .routes import (
    amazon,
    auth,
    admin,
    cart,
    checkout,
    inventory,
    messaging,
    models,
    printing,
    products,
    orgs,
    system,
    user_inventory,
)

api_router = APIRouter()
api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])
api_router.include_router(checkout.router, prefix="/checkout", tags=["checkout"])
api_router.include_router(amazon.router, prefix="/amazon", tags=["amazon"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(printing.router, prefix="/printing", tags=["printing"])
api_router.include_router(user_inventory.router, tags=["user-inventory"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(orgs.router, prefix="/orgs", tags=["orgs"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(messaging.router, tags=["messaging"])
