from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/users")
async def get_users():
    """
    Get all users
    """
    return {"message": "Get all users"}