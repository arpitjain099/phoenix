"""Main for phiphi."""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="phiphi")


class HelloWorldMessage(BaseModel):
    """HelloWorldMessage type."""

    message: str


@app.get("/")
async def root() -> HelloWorldMessage:
    """Return the hello world message."""
    return HelloWorldMessage(message="Hello World")
