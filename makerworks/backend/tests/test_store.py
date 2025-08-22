from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models import Base, Product, ProductVariant, Order, Payment
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
    r = c.post(
        "/api/v1/auth/signin", json={"email": "u@example.com", "password": "pw"}
    )
    assert r.status_code == 200


def test_store_flow(client):
    c, SessionLocal = client
    signup_signin(c)
    db = SessionLocal()
    product = Product(name="Widget")
    variant = ProductVariant(name="Default", sku="W1", price_cents=1500)
    product.variants.append(variant)
    db.add(product)
    db.commit()
    db.refresh(variant)
    db.close()

    r = c.get("/api/v1/products")
    assert r.status_code == 200
    assert r.json()[0]["name"] == "Widget"

    r = c.post(
        "/api/v1/cart/items",
        json={"product_variant_id": variant.id, "quantity": 2},
    )
    assert r.status_code == 200
    assert r.json()["items"][0]["quantity"] == 2

    with patch(
        "app.api.api_v1.routes.checkout.stripe.checkout.Session.create"
    ) as mock_create:
        mock_create.return_value = type(
            "obj", (), {"url": "http://stripe/session", "id": "sess_1"}
        )()
        r = c.post("/api/v1/checkout/session")
        assert r.status_code == 200
        assert r.json()["url"] == "http://stripe/session"

    db = SessionLocal()
    order = db.query(Order).first()
    order_id = order.id
    db.close()

    webhook_payload = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": "sess_1",
                "metadata": {"order_id": order_id},
                "amount_total": 3000,
            }
        },
    }
    with patch(
        "app.api.api_v1.routes.checkout.stripe.Webhook.construct_event"
    ) as mock_event:
        mock_event.return_value = webhook_payload
        r = c.post(
            "/api/v1/checkout/webhook",
            data="{}",
            headers={"stripe-signature": "sig"},
        )
        assert r.status_code == 200

    db = SessionLocal()
    order = db.get(Order, order_id)
    assert order.status == "paid"
    payment = db.query(Payment).filter_by(order_id=order_id).first()
    assert payment is not None
    db.close()
