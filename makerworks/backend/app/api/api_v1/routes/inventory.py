from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ....db import get_db
from ....models import InventoryLevel, InventoryMove, Product, ProductVariant
from ....inventory import provider

router = APIRouter()


class LevelPatch(BaseModel):
    sku: str
    quantity: int


@router.get("/levels")
def get_levels(db: Session = Depends(get_db)) -> list[LevelPatch]:
    levels = db.query(InventoryLevel).all()
    out: list[LevelPatch] = []
    for level in levels:
        variant = db.get(ProductVariant, level.product_variant_id)
        out.append(LevelPatch(sku=variant.sku, quantity=level.quantity))
    return out


@router.patch("/levels")
def patch_levels(data: list[LevelPatch], db: Session = Depends(get_db)) -> dict:
    for item in data:
        variant = db.query(ProductVariant).filter_by(sku=item.sku).first()
        if not variant:
            product = Product(name=item.sku)
            variant = ProductVariant(name=item.sku, sku=item.sku, price_cents=0)
            product.variants.append(variant)
            db.add(product)
            db.flush()
        level = db.query(InventoryLevel).filter_by(product_variant_id=variant.id).first()
        if not level:
            level = InventoryLevel(product_variant_id=variant.id, quantity=item.quantity)
            db.add(level)
        else:
            level.quantity = item.quantity
    db.commit()
    return {"status": "ok"}


class MoveCreate(BaseModel):
    sku: str
    delta: int
    reason: str | None = None


@router.get("/moves")
def get_moves(db: Session = Depends(get_db)) -> list[MoveCreate]:
    moves = db.query(InventoryMove).order_by(InventoryMove.created_at.desc()).all()
    out: list[MoveCreate] = []
    for move in moves:
        variant = db.get(ProductVariant, move.product_variant_id)
        out.append(
            MoveCreate(sku=variant.sku, delta=move.delta, reason=move.reason)
        )
    return out


@router.post("/moves")
def create_move(data: MoveCreate, db: Session = Depends(get_db)) -> dict:
    variant = db.query(ProductVariant).filter_by(sku=data.sku).first()
    if not variant:
        product = Product(name=data.sku)
        variant = ProductVariant(name=data.sku, sku=data.sku, price_cents=0)
        product.variants.append(variant)
        db.add(product)
        db.flush()
    level = db.query(InventoryLevel).filter_by(product_variant_id=variant.id).first()
    if not level:
        level = InventoryLevel(product_variant_id=variant.id, quantity=0)
        db.add(level)
    level.quantity += data.delta
    move = InventoryMove(
        product_variant_id=variant.id, delta=data.delta, reason=data.reason
    )
    db.add(move)
    db.commit()
    provider.record_move(data.sku, data.delta, data.reason)
    return {"id": move.id, "sku": data.sku, "delta": data.delta}
