from __future__ import annotations

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ....config import settings
from ....db import get_db
from ....models import Cart, CartItem, Order, Payment, ProductVariant, User
from ....security import get_current_user

router = APIRouter()
stripe.api_key = settings.stripe_secret_key


class SessionOut(BaseModel):
    url: str


def _get_cart(db: Session, user_id: str) -> Cart | None:
    return db.query(Cart).filter_by(user_id=user_id).first()


@router.post("/session", response_model=SessionOut)
def create_checkout_session(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    cart = _get_cart(db, user.id)
    if not cart:
        raise HTTPException(status_code=400, detail="cart empty")
    items = db.query(CartItem).filter_by(cart_id=cart.id).all()
    if not items:
        raise HTTPException(status_code=400, detail="cart empty")
    line_items = []
    total = 0
    for item in items:
        variant = db.get(ProductVariant, item.product_variant_id)
        if not variant:
            continue
        line_items.append(
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": variant.name},
                    "unit_amount": variant.price_cents,
                },
                "quantity": item.quantity,
            }
        )
        total += variant.price_cents * item.quantity
    order = Order(user_id=user.id, total_cents=total)
    db.add(order)
    db.commit()
    db.refresh(order)
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=f"{settings.frontend_url}/checkout/success",
        cancel_url=f"{settings.frontend_url}/checkout/cancel",
        metadata={"order_id": order.id},
    )
    return SessionOut(url=session.url)


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    if data.get("type") == "checkout.session.completed":
        session = data["data"]["object"]
        order_id = session["metadata"]["order_id"]
        order = db.get(Order, order_id)
        if order and order.status != "paid":
            order.status = "paid"
            payment = Payment(
                order_id=order.id,
                provider="stripe",
                provider_payment_id=session["id"],
                amount_cents=session.get("amount_total", order.total_cents),
                status="succeeded",
            )
            db.add(payment)
            db.commit()
    return {"status": "ok"}
