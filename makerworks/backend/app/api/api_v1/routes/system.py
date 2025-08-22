from fastapi import APIRouter, Depends

from app.api.deps import rate_limiter, require_api_key

router = APIRouter()


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/limited", dependencies=[Depends(rate_limiter(2, 1))])
async def limited() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/secure", dependencies=[Depends(require_api_key)])
def secure() -> dict[str, str]:
    return {"secret": "data"}
