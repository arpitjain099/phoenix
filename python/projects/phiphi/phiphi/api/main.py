"""Main for phiphi."""
import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from phiphi import config, utils
from phiphi.api import health_check, insecure_auth
from phiphi.api.environments import routes as environment_routes
from phiphi.api.projects import routes as project_routes
from phiphi.api.projects.gathers import routes as gather_routes
from phiphi.api.projects.job_runs import routes as job_runs_routes
from phiphi.api.users import routes as user_routes

utils.init_logging()

logger = logging.getLogger(__name__)

app = FastAPI(title=config.settings.TITLE)

app.include_router(health_check.router)
if config.settings.INCLUDE_INSECURE_AUTH:
    logger.info("Including insecure auth routes.")
    app.include_router(insecure_auth.router)
app.include_router(user_routes.router, tags=["User"])
app.include_router(environment_routes.router, tags=["Environment"])
app.include_router(project_routes.router, tags=["Project"])
app.include_router(gather_routes.router, tags=["Project Gathers"])
app.include_router(job_runs_routes.router, tags=["Project Job Runs"])

if config.settings.CORS_ORIGINS:
    logger.info("Adding CORS middleware.")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).strip("/") for origin in config.settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

logger.info("Phiphi FastAPI started.")
