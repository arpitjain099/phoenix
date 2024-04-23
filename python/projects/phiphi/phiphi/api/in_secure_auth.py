"""Health check for the application."""

from fastapi import APIRouter, status

from phiphi import config

router = APIRouter()


@router.get(
    "/oauth2/in_secure_auth",
    response_model=dict,
    tags=["oauth"],
    status_code=status.HTTP_202_ACCEPTED,
)
async def in_secure_auth() -> dict:
    """This route will be used for a local cluster to be run without oauth2 implement."""
    headers = {
        "Gap-Auth": config.settings.FIRST_ADMIN_USER_EMAIL,
        "X-Auth-Request-Email": config.settings.FIRST_ADMIN_USER_EMAIL,
        "X-Auth-Request-User": "1",
    }

    return headers
