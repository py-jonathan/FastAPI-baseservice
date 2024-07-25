from fastapi import APIRouter, HTTPException
from models.users import User

router = APIRouter()

@router.get("/users")
async def get_users(page: int):
    """
    Get all users with pagination max = 10
    """
    total_users = await User.count()
    users = await User.find().skip(page * 10).limit(10).to_list()
    data = {
        "total_users": total_users,
        "users": [user.model_dump(include=("username", "email", "role", "created")) for user in users]
    }
    return data