from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models import Base, User
from app.db import get_db


@pytest.fixture()
def client_and_session():
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


def test_org_and_dm_activity(client_and_session):
    client, SessionLocal = client_and_session

    r = client.post('/api/v1/auth/signup', json={'email': 'a@example.com', 'password': 'pw'})
    admin_id = r.json()['id']
    r = client.post('/api/v1/auth/signup', json={'email': 'b@example.com', 'password': 'pw'})
    user2_id = r.json()['id']

    # promote to admin
    db = SessionLocal()
    admin = db.get(User, admin_id)
    admin.role = 'admin'
    db.commit()
    db.close()

    client.post('/api/v1/auth/signin', json={'email': 'a@example.com', 'password': 'pw'})

    r = client.post('/api/v1/orgs', json={'name': 'Org1'})
    assert r.status_code == 200

    with client.websocket_connect(f'/api/v1/ws/dm/{user2_id}') as ws2:
        with client.websocket_connect(f'/api/v1/ws/dm/{admin_id}') as ws1:
            ws1.send_json({'to': user2_id, 'message': 'hi'})
            data = ws2.receive_json()
            assert data == {'from': admin_id, 'message': 'hi'}

    r = client.get('/api/v1/admin/activity')
    assert r.status_code == 200
    actions = [e['action'] for e in r.json()]
    assert 'org_created' in actions
    assert 'dm' in actions
