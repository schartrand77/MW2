from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ....db import get_db
from ....models import Cart, CartItem, ProductVariant, User
from ....security import get_current_user

router = APIRouter()


class CartItemOut(BaseModel):
    id: str
    product_variant_id: str
    quantity: int

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    id: str
    items: list[CartItemOut]


class AddItem(BaseModel):
    product_variant_id: str
    quantity: int = 1


def _get_or_create_cart(db: Session, user_id: str) -> Cart:
    cart = db.query(Cart).filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.get("/", response_model=CartOut)
def get_cart(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = _get_or_create_cart(db, user.id)
    items = db.query(CartItem).filter_by(cart_id=cart.id).all()
    return CartOut(id=cart.id, items=items)


@router.post("/items", response_model=CartOut)
def add_item(
    data: AddItem,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart = _get_or_create_cart(db, user.id)
    variant = db.get(ProductVariant, data.product_variant_id)
    if not variant:
        raise HTTPException(status_code=404, detail="variant not found")
    item = (
        db.query(CartItem)
        .filter_by(cart_id=cart.id, product_variant_id=variant.id)
        .first()
    )
    if item:
        item.quantity += data.quantity
    else:
        item = CartItem(
            cart_id=cart.id,
            product_variant_id=variant.id,
            quantity=data.quantity,
        )
        db.add(item)
    db.commit()
    items = db.query(CartItem).filter_by(cart_id=cart.id).all()
    return CartOut(id=cart.id, items=items)
