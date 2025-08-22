from __future__ import annotations

from .base import PrinterConnector


class BambuConnector(PrinterConnector):
    def __init__(self, api_key: str | None) -> None:
        self.api_key = api_key

    def submit_job(self, model: str) -> str:
        return "bambu-job-1"

    def get_status(self, job_id: str) -> dict:
        return {"id": job_id, "status": "printing"}

    def handle_webhook(self, data: dict) -> None:
        return None

