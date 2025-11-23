from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID
from app.utils.database import supabase
from app import schemas

router = APIRouter(prefix="/folders", tags=["Folders"])

@router.get("/", response_model=List[schemas.Folder])
def get_all_folders():
    response = supabase.table("folders").select("*").execute()
    return response.data

@router.get("/{folder_id}", response_model=schemas.Folder)
def get_folder(folder_id: UUID):
    response = supabase.table("folders").select("*").eq("folder_id", str(folder_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Folder not found")
    return response.data[0]

@router.post("/", response_model=schemas.Folder, status_code=status.HTTP_201_CREATED)
def create_folder(folder: schemas.FolderCreate):
    data = folder.model_dump(exclude_unset=True)
    if data.get('user_id'): data['user_id'] = str(data['user_id'])
    if data.get('parent_folder_id'): data['parent_folder_id'] = str(data['parent_folder_id'])
    
    response = supabase.table("folders").insert(data).execute()
    return response.data[0]

@router.put("/{folder_id}", response_model=schemas.Folder)
def update_folder(folder_id: UUID, folder: schemas.FolderUpdate):
    data = folder.model_dump(exclude_unset=True)
    if data.get('parent_folder_id'): data['parent_folder_id'] = str(data['parent_folder_id'])

    response = supabase.table("folders").update(data).eq("folder_id", str(folder_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Folder not found")
    return response.data[0]

@router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_folder(folder_id: UUID):
    supabase.table("folders").delete().eq("folder_id", str(folder_id)).execute()
    return None
