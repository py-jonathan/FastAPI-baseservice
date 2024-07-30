from fastapi import APIRouter
from .admin_routes import router as admin_router
from .ai_routes import router as ai_router
from .auth_routes import router as auth_router
from .users_routes import router as user_router

router = APIRouter(prefix="/api/v1")
router.include_router(admin_router, tags=["admin"], prefix="/admin")
router.include_router(ai_router, tags=["ai"], prefix="/ai")
router.include_router(auth_router, tags=["auth"], prefix="/auth")
router.include_router(user_router, tags=["users"], prefix="/users")
