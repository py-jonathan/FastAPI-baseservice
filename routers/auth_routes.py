from fastapi import APIRouter, Depends, HTTPException
from schemas.users import (
    UserLogin,
    UserRegistration,
    UserProfileUpdate,
    UserResetPassword,
)
from models.users import User
from utils.security import hash_password, verify_password
from auth.jwt import create_access_token, get_current_user

router = APIRouter()

@router.post("/register")
async def register_user(user_input: UserRegistration):
    hashed_password = hash_password(user_input.password)
    user = User(**user_input.model_dump(exclude=("password")), password=hashed_password)
    await user.create()
    return user

@router.post("/login")
async def login_user(user_input: UserLogin):
    user = await User.find_by_email(user_input.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(user_input.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout_user():
    return {"message": "Logout successful"}

@router.post("/reset-password")
async def reset_password(user_input: UserResetPassword):
    user: User = await User.find_by_email(user_input.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(user_input.old_password, user.password):
        raise HTTPException(status_code=400, detail="Invalid old password")
    user.password = hash_password(user_input.new_password)
    await user.save()
    return user

@router.put("/update-profile")
async def update_profile(user_input: UserProfileUpdate, current_user: User = Depends(get_current_user)):
    user = await User.find_by_email(current_user.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    fields = user_input.model_dump(exclude_none=True)
    for field, value in fields.items():
        setattr(user, field, value)
    await user.save()
    return user
