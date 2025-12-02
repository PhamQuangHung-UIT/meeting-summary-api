from fastapi import APIRouter, HTTPException, status
from typing import List

from app.utils.database import supabase
from app import schemas

router = APIRouter(prefix="/recording_tags", tags=["Recording Tags"])

@router.get("/", response_model=List[schemas.RecordingTag])
def get_all_recording_tags():
    response = supabase.table("recording_tags").select("*").execute()
    return response.data

@router.get("/{id}", response_model=schemas.RecordingTag)
def get_recording_tag(id: str):
    response = supabase.table("recording_tags").select("*").eq("id", id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Recording Tag not found")
    return response.data[0]

@router.post("/", response_model=schemas.RecordingTag, status_code=status.HTTP_201_CREATED)
def create_recording_tag(tag: schemas.RecordingTagCreate):
    data = tag.model_dump(mode='json', exclude_unset=True)
    response = supabase.table("recording_tags").insert(data).execute()
    return response.data[0]

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recording_tag(id: str):
    supabase.table("recording_tags").delete().eq("id", id).execute()
    return None
