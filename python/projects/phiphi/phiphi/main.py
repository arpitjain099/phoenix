"""Main for phiphi."""
from fastapi import FastAPI

from phiphi import health_check
from phiphi.core import config
from phiphi.users import routes as user_routes

app = FastAPI(title=config.settings.TITLE)

app.include_router(health_check.router)
app.include_router(user_routes.router)
