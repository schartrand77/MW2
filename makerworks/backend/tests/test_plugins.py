import os
from fastapi.testclient import TestClient


def test_plugin_loaded(monkeypatch):
    monkeypatch.setenv("POSTGRES_URL", "sqlite:///./test.db")
    monkeypatch.setenv("PLUGINS", "tests.sample_plugin")

    import importlib
    from prometheus_client import REGISTRY
    for collector in list(REGISTRY._collector_to_names):  # type: ignore[attr-defined]
        try:
            REGISTRY.unregister(collector)
        except KeyError:
            pass
    import app.config as config
    importlib.reload(config)
    import app.main as main
    importlib.reload(main)

    app = main.create_app()
    client = TestClient(app)
    r = client.get("/plugin/hello")
    assert r.status_code == 200
    assert r.json() == {"msg": "hi"}
