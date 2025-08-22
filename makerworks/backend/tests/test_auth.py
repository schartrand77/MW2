from __future__ import annotations

import pyotp
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models import Base
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
        yield c
    app.dependency_overrides.clear()


def test_signup_signin_totp_flow(client: TestClient):
    r = client.post(
        "/api/v1/auth/signup", json={"email": "u@example.com", "password": "pw"}
    )
    assert r.status_code == 200

    r = client.post(
        "/api/v1/auth/signin", json={"email": "u@example.com", "password": "pw"}
    )
    assert r.status_code == 200
    csrf = r.cookies.get("csrf")

    r = client.get("/api/v1/auth/me")
    assert r.status_code == 200
    assert r.json()["email"] == "u@example.com"

    r = client.post("/api/v1/auth/totp/setup")
    secret = r.json()["secret"]
    code = pyotp.TOTP(secret).now()
    r = client.post(
        "/api/v1/auth/totp/verify", json={"secret": secret, "code": code}
    )
    assert r.status_code == 200

    r = client.post(
        "/api/v1/auth/signout", headers={"X-CSRF-Token": csrf}
    )
    assert r.status_code == 200

    r = client.post(
        "/api/v1/auth/signin", json={"email": "u@example.com", "password": "pw"}
    )
    assert r.status_code == 400

    code = pyotp.TOTP(secret).now()
    r = client.post(
        "/api/v1/auth/signin",
        json={"email": "u@example.com", "password": "pw", "otp": code},
    )
    assert r.status_code == 200
