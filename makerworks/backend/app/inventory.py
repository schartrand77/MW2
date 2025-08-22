from __future__ import annotations

from abc import ABC, abstractmethod


class InventoryProvider(ABC):
    @abstractmethod
    def record_move(self, sku: str, delta: int, reason: str | None = None) -> None:
        """Record inventory movement to an external system."""
        raise NotImplementedError


class DummyProvider(InventoryProvider):
    def record_move(self, sku: str, delta: int, reason: str | None = None) -> None:  # pragma: no cover - stub
        return None


provider: InventoryProvider = DummyProvider()
