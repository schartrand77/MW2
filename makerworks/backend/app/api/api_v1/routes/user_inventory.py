from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ....db import get_db
from ....models import ProductVariant, UserInventory, User
from ....security import get_current_user

router = APIRouter()


class ItemIn(BaseModel):
    sku: str
    quantity: int


@router.get("/user/inventory")
def list_inventory(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> list[dict[str, int | str]]:
    items = db.query(UserInventory).filter_by(user_id=user.id).all()
    out = []
    for item in items:
        variant = db.get(ProductVariant, item.product_variant_id)
        out.append({"id": item.id, "sku": variant.sku, "quantity": item.quantity})
    return out


@router.post("/user/inventory")
def upsert_inventory(
    data: ItemIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> dict:
    variant = db.query(ProductVariant).filter_by(sku=data.sku).first()
    if not variant:
        raise HTTPException(status_code=404, detail="variant not found")
    item = (
        db.query(UserInventory)
        .filter_by(user_id=user.id, product_variant_id=variant.id)
        .first()
    )
    if item:
        item.quantity = data.quantity
    else:
        item = UserInventory(
            user_id=user.id, product_variant_id=variant.id, quantity=data.quantity
        )
        db.add(item)
    db.commit()
    return {"id": item.id, "sku": variant.sku, "quantity": item.quantity}


@router.delete("/user/inventory/{item_id}")
def delete_inventory(
    item_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> dict:
    item = db.get(UserInventory, item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404)
    db.delete(item)
    db.commit()
    return {"status": "deleted"}
