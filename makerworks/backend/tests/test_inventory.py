from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models import Base, Product, ProductVariant
from app.db import get_db


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c, TestingSessionLocal
    app.dependency_overrides.clear()


def signup_signin(c: TestClient):
    c.post("/api/v1/auth/signup", json={"email": "u@example.com", "password": "pw"})
    r = c.post("/api/v1/auth/signin", json={"email": "u@example.com", "password": "pw"})
    assert r.status_code == 200


def test_inventory_flow(client):
    c, SessionLocal = client
    signup_signin(c)
    db = SessionLocal()
    product = Product(name="Widget")
    variant = ProductVariant(name="Default", sku="S1", price_cents=100)
    product.variants.append(variant)
    db.add(product)
    db.commit()
    db.refresh(variant)
    db.close()

    r = c.post("/api/v1/inventory/moves", json={"sku": "S1", "delta": 5})
    assert r.status_code == 200
    r = c.get("/api/v1/inventory/levels")
    assert r.json()[0]["quantity"] == 5

    r = c.patch("/api/v1/inventory/levels", json=[{"sku": "S1", "quantity": 10}])
    assert r.status_code == 200
    r = c.get("/api/v1/inventory/levels")
    assert r.json()[0]["quantity"] == 10

    r = c.post("/api/v1/user/inventory", json={"sku": "S1", "quantity": 2})
    assert r.status_code == 200
    item_id = r.json()["id"]
    r = c.get("/api/v1/user/inventory")
    assert len(r.json()) == 1
    r = c.delete(f"/api/v1/user/inventory/{item_id}")
    assert r.status_code == 200
