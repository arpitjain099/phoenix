"""Main for phiphi."""
from fastapi import FastAPI

app = FastAPI(title="phiphi")


@app.get("/")
async def root():
    """Return the hello world message."""
    return {"message": "Hello World"}
