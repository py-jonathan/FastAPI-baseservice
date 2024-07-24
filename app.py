"""Server app config."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from endpoints import endpoint_manager
from routers import router as routers
from routers.elasticsearch import router as elasticsearch_router
from routers.websocket import router as websocket_router
from fastapi.responses import JSONResponse
from middlewares.rate_limit import RateLimitMiddleware

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
app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60, max_ips=10000)

app.include_router(routers)
app.include_router(elasticsearch_router, prefix="/search", tags=["Search"])
app.include_router(websocket_router, prefix="/ws", tags=["WebSocket"])
