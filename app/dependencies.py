from fastapi import Depends, HTTPException

from app.auth import verify_access_token


# Get logged-in user from JWT
def get_current_user(token_data=Depends(verify_access_token)):
    return token_data


# Allow only Admin users
def admin_required(current_user=Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user


# Allow Admin or Manager
def manager_required(current_user=Depends(get_current_user)):

    if current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(
            status_code=403,
            detail="Manager access required"
        )

    return current_user