from fastapi import HTTPException, status, Header
from app.core.config import settings


async def verify_api_key(xapi_key: str = Header(...)) -> str:
    if xapi_key != settings.API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or missing API Key",
                            )
    return xapi_key


async def get_idempotency_key(idempotency_key: str = Header(...)) -> str:
    if not idempotency_key or not idempotency_key.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Idempotency-Key header is required",
                            )
    return idempotency_key
