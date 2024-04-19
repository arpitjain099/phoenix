"""Main for phiphi."""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from phiphi import config
from phiphi.api import health_check
from phiphi.api.environments import routes as environment_routes
from phiphi.api.projects import routes as project_routes
from phiphi.api.projects.gathers import routes as gather_routes
from phiphi.api.projects.project_runs import routes as project_runs_routes
from phiphi.api.users import routes as user_routes

app = FastAPI(title=config.settings.TITLE)

app.include_router(health_check.router)
app.include_router(user_routes.router, tags=["User"])
app.include_router(environment_routes.router, tags=["Environment"])
app.include_router(project_routes.router, tags=["Project"])
app.include_router(gather_routes.router, tags=["Project Gathers"])
app.include_router(project_runs_routes.router, tags=["Project Runs"])

if config.settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).strip("/") for origin in config.settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
