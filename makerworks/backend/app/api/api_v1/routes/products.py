from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ....db import get_db
from ....models import Product, ProductVariant, User
from ....security import get_current_user

router = APIRouter()


class VariantOut(BaseModel):
    id: str
    name: str
    sku: str
    price_cents: int

    class Config:
        from_attributes = True


class ProductOut(BaseModel):
    id: str
    name: str
    description: str | None
    variants: list[VariantOut] = []

    class Config:
        from_attributes = True


class VariantCreate(BaseModel):
    name: str
    sku: str
    price_cents: int


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    variants: list[VariantCreate]


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403)
    return user


@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404)
    return product


@router.post("/", response_model=ProductOut)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    product = Product(name=data.name, description=data.description)
    for v in data.variants:
        product.variants.append(
            ProductVariant(name=v.name, sku=v.sku, price_cents=v.price_cents)
        )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
