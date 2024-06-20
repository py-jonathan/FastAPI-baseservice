"""
User schemas  - Pydantic models for user registration, login and update
User registration schema
User login schema
User update schema
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserRegistration(BaseModel):
    """
    User registration schema
    """
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

class UserLogin(BaseModel):
    """
    User login schema
    """
    email: EmailStr = Field(...)
    password: str = Field(...)

class UserProfileUpdate(BaseModel):
    """
    User profile update schema
    """
    email: EmailStr = Field(...)
    fullname: Optional[str] = Field(None)
    avatar: Optional[str] = Field(None)
    bio: Optional[str] = Field(None)
    website: Optional[str] = Field(None)
    location: Optional[str] = Field(None)
    gender: Optional[str] = Field(None)


class UserResetPassword(BaseModel):
    """
    User reset password schema
    """
    email: EmailStr = Field(...)
    old_password: str = Field(...)
    new_password: str = Field(...)
