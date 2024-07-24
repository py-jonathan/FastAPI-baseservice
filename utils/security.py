"""Password utility functions."""

import bcrypt
import hashlib
import os
from models.users import User
from datetime import datetime, timedelta,timezone
from typing import Tuple,Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

# commom way to hash password and verify password
# bcrypt is designed to be secure and slow to thwart brute-force attacks, no system is entirely immune to attacks.

def hash_password(password: str) -> str:
    """Return a salted password hash."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """Return True if password matches hash."""
    return bcrypt.checkpw(password.encode(), hashed.encode())


# you can store salt and hashed password in the database
# attacker need password and salt to crack the password


def hash_password_with_salt(password: str, salt: Optional[bytes] = None) -> Tuple[bytes, str]:
    if salt is None:
        salt = os.urandom(16)  # 16 bytes salt
    hash = hashlib.sha256(salt + password.encode()).hexdigest()
    return salt, hash

# JWT-related functions
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def is_token_expired(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expiration = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)
        return datetime.now(timezone.utc) > expiration
    except JWTError:
        return True

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current user from the JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await User.find_one(User.username == username)
    if user is None:
        raise credentials_exception
    return user