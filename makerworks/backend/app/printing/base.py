from __future__ import annotations

from abc import ABC, abstractmethod


class PrinterConnector(ABC):
    @abstractmethod
    def submit_job(self, model: str) -> str:  # pragma: no cover - interface
        ...

    @abstractmethod
    def get_status(self, job_id: str) -> dict:  # pragma: no cover - interface
        ...

    @abstractmethod
    def handle_webhook(self, data: dict) -> None:  # pragma: no cover - interface
        ...

