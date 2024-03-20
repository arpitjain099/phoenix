"""Main for phiphi."""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from phiphi import health_check
from phiphi.core import config
from phiphi.users import routes as user_routes

app = FastAPI(title=config.settings.TITLE)

app.include_router(health_check.router)
app.include_router(user_routes.router)

if config.settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).strip("/") for origin in config.settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
