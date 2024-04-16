"""Main for phiphi."""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from phiphi import config
from phiphi.api import health_check
from phiphi.api.environments import routes as environment_routes
from phiphi.api.instances import routes as instance_routes
from phiphi.api.instances.gathers import routes as gather_routes
from phiphi.api.instances.instance_runs import routes as instance_runs_routes
from phiphi.api.users import routes as user_routes

app = FastAPI(title=config.settings.TITLE)

app.include_router(health_check.router)
app.include_router(user_routes.router, tags=["User"])
app.include_router(environment_routes.router, tags=["Environment"])
app.include_router(instance_routes.router, tags=["Instance"])
app.include_router(gather_routes.router, tags=["Instance Gathers"])
app.include_router(instance_runs_routes.router, tags=["Instance Runs"])

if config.settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).strip("/") for origin in config.settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
