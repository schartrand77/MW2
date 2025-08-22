from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db import get_db
from app.models import Base, FeatureFlag
from app.config import settings


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


def test_amazon_feature_flag(client: TestClient):
    r = client.get("/api/v1/amazon/search", params={"q": "filament"})
    assert r.status_code == 404

    settings.amazon_associate_tag = "testtag"
    # enable flag
    db = next(app.dependency_overrides[get_db]())
    db.add(FeatureFlag(key="amazon_affiliate", enabled=True))
    db.commit()
    db.close()

    r = client.get("/api/v1/amazon/search", params={"q": "filament"})
    assert r.status_code == 200
    url = r.json()["items"][0]["url"]
    assert "tag=testtag" in url
