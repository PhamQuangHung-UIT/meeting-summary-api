from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from app.utils.database import supabase
from pydantic import BaseModel
from app.services.user_service import UserService
from app import schemas

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> schemas.User:
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
             raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = user_response.user.id
        user = UserService.get_user_by_id(user_id)
        if not user:
            # If user is in Auth but not in public.users table, we might need to handle it.
            # For now, let's assume they must exist in the users table.
            raise HTTPException(status_code=401, detail="User profile not found")
        
        return schemas.User(**user)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

class RoleChecker:
    def __init__(self, allowed_roles: List[schemas.UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: schemas.User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have enough permissions"
            )
        return user

router = APIRouter(prefix="/auth", tags=["auth"])

class UserSignupRequest(BaseModel):
    full_name: str | None = None
    email: str
    password: str


@router.post("/login", summary="Login user with Supabase")
def login_user(email: str, password: str):
    """Login a user with Supabase."""
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response:
            return {"status": "success", "user": response}
    except Exception:
        pass
        
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/signup", summary="Sign up user with Supabase")
def signup_user(request: UserSignupRequest):
    """Sign up a user with Supabase."""
    try:
        response = supabase.auth.sign_up({"email": request.email, "password": request.password})
        if response:
            # Create user profile in users table if needed
            # Usually handled by Supabase Trigger, but we can do it here if not.
            # For now, let's just return success.
            return {"status": "success", "user": response}
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error signing up user: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error signing up user",
        headers={"WWW-Authenticate": "Bearer"},
    )
