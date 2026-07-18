from datetime import datetime, timedelta

from jose import JWTError, jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


# Secret key used to sign JWT
SECRET_KEY = "your-secret-key-change-this"

# Algorithm used for JWT
ALGORITHM = "HS256"

# Token expires after 30 minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Read Bearer Token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# -----------------------------
# Create JWT Token
# -----------------------------
def create_access_token(data: dict):

    # Copy user data
    to_encode = data.copy()

    # Add expiry time
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Add expiry into payload
    to_encode["exp"] = expire

    # Generate JWT
    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# -----------------------------
# Verify JWT Token
# -----------------------------
def verify_access_token(
    token: str = Depends(oauth2_scheme)
):

    try:

        # Decode JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Return decoded user data
        return payload

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )