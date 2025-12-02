from fastapi import APIRouter, HTTPException, status
from typing import List

from app import schemas
from app.services.folder_service import FolderService

router = APIRouter(prefix="/folders", tags=["Folders"])

@router.get("/", response_model=List[schemas.Folder])
def get_all_folders():
    return FolderService.get_all_folders()

@router.get("/{folder_id}", response_model=schemas.Folder)
def get_folder(folder_id: str):
    folder = FolderService.get_folder_by_id(folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder

@router.post("/", response_model=schemas.Folder, status_code=status.HTTP_201_CREATED)
def create_folder(folder: schemas.FolderCreate):
    return FolderService.create_folder(folder)

@router.put("/{folder_id}", response_model=schemas.Folder)
def update_folder(folder_id: str, folder: schemas.FolderUpdate):
    updated_folder = FolderService.update_folder(folder_id, folder)
    if not updated_folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return updated_folder

@router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_folder(folder_id: str):
    FolderService.delete_folder(folder_id)
    return None
