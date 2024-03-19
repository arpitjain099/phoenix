"""Health check for the application."""
import pydantic
from fastapi import APIRouter

from phiphi.core import config

router = APIRouter()


class HealthCheck(pydantic.BaseModel):
    """HealthCheck."""

    title: str
    version: str


@router.get("/", response_model=HealthCheck, tags=["status"])
async def health_check() -> HealthCheck:
    """HealthCheck."""
    return HealthCheck(
        title=config.settings.TITLE,
        version=config.settings.VERSION,
    )
