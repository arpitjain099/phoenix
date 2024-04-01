"""Main for phiphi."""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from phiphi import config
from phiphi.api import health_check
from phiphi.api.users import routes as user_routes
from phiphi.api.instances import routes as instance_routes

app = FastAPI(title=config.settings.TITLE)

app.include_router(health_check.router)
app.include_router(user_routes.router, tags=["User"])
app.include_router(instance_routes.router, tags=["Instance"])

if config.settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).strip("/") for origin in config.settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
