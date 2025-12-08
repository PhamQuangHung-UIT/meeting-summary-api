from typing import List
from fastapi import APIRouter, HTTPException, status
from app.utils.database import supabase
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class UserSignupRequest(BaseModel):
    name: str | None = None
    email: str
    password: str


@router.post("/login", summary="Login user with Supabase")
def login_user(email: str, password: str):
    """Login a user with Supabase."""
    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if response:
        return {"status": "success", "user": response}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/signup", summary="Sign up user with Supabase")
def signup_user(request: UserSignupRequest):
    """Sign up a user with Supabase."""
    response = supabase.auth.sign_up({"email": request.email, "password": request.password})
    if response:
        return {"status": "success", "user": response}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error signing up user",
        headers={"WWW-Authenticate": "Bearer"},
    )
