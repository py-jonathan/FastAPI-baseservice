"""Server app config."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from endpoints import endpoint_manager
from routers import router as routers

DESCRIPTION = """
This API powers whatever I want to make

It supports: ...
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application services."""
    await endpoint_manager.connect()
    print("Startup complete")
    yield
    print("Shutdown complete")


app = FastAPI(
    title="My Server",
    description=DESCRIPTION,
    version="0.1.0",
    contact={
        "name": "Hello World Jr",
        "url": "https://myserver.dev",
        "email": "helloworld@myserver.dev",
    },
    license_info={
        "name": "MIT",
        "url": "...",
    },
    lifespan=lifespan,
)

app.include_router(routers)
