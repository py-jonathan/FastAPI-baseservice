"""Server app config."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from endpoints import endpoint_manager
from routers import admin_routes, ai_routes, auth_routes, users_routes
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

# Include routers
app.include_router(admin_routes, prefix="/admin", tags=["Admin"])
app.include_router(ai_routes, prefix="/ai", tags=["AI"])
app.include_router(auth_routes, prefix="/auth", tags=["Auth"])
app.include_router(users_routes, prefix="/users", tags=["Users"])

# Note: The elasticsearch_router has been removed as it's not in your current structure