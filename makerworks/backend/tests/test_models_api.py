from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models import Base
from app.db import get_db

UPLOAD_DIR = Path(__file__).resolve().parents[3] / 'uploads'
THUMB_DIR = Path(__file__).resolve().parents[3] / 'thumbnails'


@pytest.fixture()
def client():
    engine = create_engine(
        'sqlite:///:memory:',
        future=True,
        connect_args={'check_same_thread': False},
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
    for p in UPLOAD_DIR.glob('*'):
        if p.is_file():
            p.unlink()
    for p in THUMB_DIR.glob('*'):
        if p.is_file():
            p.unlink()


def signup(c: TestClient):
    c.post('/api/v1/auth/signup', json={'email': 'u@example.com', 'password': 'pw'})
    c.post('/api/v1/auth/signin', json={'email': 'u@example.com', 'password': 'pw'})


def test_model_upload_and_color(client: TestClient):
    c = client
    signup(c)
    with open('test.stl', 'rb') as f:
        r = c.post('/api/v1/models', files={'file': ('test.stl', f, 'model/stl')})
    assert r.status_code == 200
    model_id = r.json()['id']

    r = c.get('/api/v1/models')
    assert r.status_code == 200
    assert r.json()[0]['id'] == model_id

    r = c.post(f'/api/v1/models/{model_id}/color', json={'color': '#00ff00'})
    assert r.status_code == 200
    assert r.json()['thumbnail']

    r = c.post(f'/api/v1/models/{model_id}/rethumb')
    assert r.status_code == 200
