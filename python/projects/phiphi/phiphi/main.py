"""Main for phiphi."""
from fastapi import FastAPI

from phiphi import health
from phiphi.core import config

app = FastAPI(title=config.settings.TITLE)

app.include_router(health.router)
