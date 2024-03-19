"""Main for phiphi."""
from fastapi import FastAPI

from phiphi import health_check
from phiphi.core import config

app = FastAPI(title=config.settings.TITLE)

app.include_router(health_check.router)
