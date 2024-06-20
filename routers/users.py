"""
Regestration router
"""

from fastapi import APIRouter, HTTPException
from schemas.users import (
    UserLogin,
    UserRegistration,
    UserProfileUpdate,
    UserResetPassword,
)
from models.users import User
from utils.security import hash_password, verify_password

router = APIRouter()


@router.post("/register")
async def register_user(user_input: UserRegistration):
    """
    Register a new user
    """
    # check email and username
    # user = await User.find_by_email(user_input.email)
    # user = await User.find("email" == user_input.email)
    # if user:
    #     raise HTTPException(status_code=400, detail="Email already exists")
    # else:
    hashed_password = hash_password(user_input.password)
    user = User(**user_input.model_dump(exclude=("password")), password=hashed_password)
    await user.create()
    return user


@router.post("/login")
async def login_user(user_input: UserLogin):
    """
    Login user
    """
    user = await User.find_by_email(user_input.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(user_input.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    return user


@router.post("/logout")
async def logout_user():
    """
    Logout user
    """
    return {"message": "Logout successful"}


@router.post("/reset-password")
async def reset_password(user_input: UserResetPassword):
    """
    Reset user password
    """
    user: User = await User.find_by_email(user_input.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(user_input.old_password, user.password):
        raise HTTPException(status_code=400, detail="Invalid old password")
    user.password = hash_password(user_input.new_password)
    await user.save()
    return user


@router.put("/update-profile")
async def update_profile(user_input: UserProfileUpdate):
    """
    Update user profile
    """
    user: User = await User.find_by_email(user_input.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    else:
        fields = user_input.model_dump(exclude_none=True)
        user = user.model_copy(fields)
        await user.save()
        return user
