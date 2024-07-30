"""Password utility functions."""

import bcrypt
import hashlib
import os


def hash_password(password: str) -> str:
    """Return a salted password hash using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Return True if password matches the hash using bcrypt."""
    return bcrypt.checkpw(password.encode(), hashed.encode())



def hash_password_with_salt(password: str, salt: bytes = None) -> tuple[bytes, str]:
    """Return a tuple of salt and SHA-256 hashed password."""
    if salt is None:
        salt = os.urandom(16)  
    hash = hashlib.sha256(salt + password.encode()).hexdigest()
    return salt, hash

def verify_password_with_salt(stored_salt: bytes, stored_hash: str, input_password: str) -> bool:
    """Return True if the input password matches the stored hash when hashed with the stored salt."""
    _, hash = hash_password_with_salt(input_password, stored_salt)
    return hash == stored_hash
