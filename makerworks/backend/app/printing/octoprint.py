from __future__ import annotations

from .base import PrinterConnector


class OctoPrintConnector(PrinterConnector):
    def __init__(self, base_url: str | None, api_key: str | None) -> None:
        self.base_url = base_url
        self.api_key = api_key

    def submit_job(self, model: str) -> str:
        return "octo-job-1"

    def get_status(self, job_id: str) -> dict:
        return {"id": job_id, "status": "queued"}

    def handle_webhook(self, data: dict) -> None:
        return None

