from fastapi import APIRouter, HTTPException, status
from typing import List

from app.utils.database import supabase
from app import schemas

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[schemas.User])
def get_all_users():
    response = supabase.table("users").select("*").execute()
    return response.data

@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: str):
    response = supabase.table("users").select("*").eq("user_id", user_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate):
    response = supabase.table("users").insert(user.model_dump(exclude_unset=True)).execute()
    return response.data[0]

@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: str, user: schemas.UserUpdate):
    response = supabase.table("users").update(user.model_dump(exclude_unset=True)).eq("user_id", user_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    supabase.table("users").delete().eq("user_id", user_id).execute()
    return None
