from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from ....printing import get_connector

router = APIRouter()


class JobRequest(BaseModel):
    model: str


@router.post("/{provider}/jobs")
def submit_job(provider: str, job: JobRequest) -> dict:
    try:
        connector = get_connector(provider)
    except ValueError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=404) from exc
    job_id = connector.submit_job(job.model)
    return {"id": job_id}


@router.get("/{provider}/jobs/{job_id}")
def job_status(provider: str, job_id: str) -> dict:
    try:
        connector = get_connector(provider)
    except ValueError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=404) from exc
    return connector.get_status(job_id)


@router.post("/{provider}/webhook")
async def webhook(provider: str, request: Request) -> dict:
    try:
        connector = get_connector(provider)
    except ValueError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=404) from exc
    data = await request.json()
    connector.handle_webhook(data)
    return {"status": "ok"}

