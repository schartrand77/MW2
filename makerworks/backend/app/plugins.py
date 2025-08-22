from importlib import import_module
from typing import Iterable

from fastapi import FastAPI


def load_plugins(app: FastAPI, plugins: Iterable[str]) -> None:
    """Import plugin modules and call their setup(app) hooks."""
    for path in plugins:
        try:
            module = import_module(path)
            setup = getattr(module, "setup", None)
            if callable(setup):
                setup(app)
        except Exception as exc:  # pragma: no cover - log and continue
            print(f"Failed to load plugin {path}: {exc}")
