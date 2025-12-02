from fastapi import APIRouter, HTTPException, status
from typing import List

from app.utils.database import supabase
from app import schemas

router = APIRouter(prefix="/recordings", tags=["Recordings"])

@router.get("/", response_model=List[schemas.Recording])
def get_all_recordings():
    response = supabase.table("recordings").select("*").execute()
    return response.data

@router.get("/{recording_id}", response_model=schemas.Recording)
def get_recording(recording_id: str):
    response = supabase.table("recordings").select("*").eq("recording_id", recording_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Recording not found")
    return response.data[0]

@router.post("/", response_model=schemas.Recording, status_code=status.HTTP_201_CREATED)
def create_recording(recording: schemas.RecordingCreate):
    data = recording.model_dump(exclude_unset=True)
    response = supabase.table("recordings").insert(data).execute()
    return response.data[0]

@router.put("/{recording_id}", response_model=schemas.Recording)
def update_recording(recording_id: str, recording: schemas.RecordingUpdate):
    data = recording.model_dump(exclude_unset=True)
    response = supabase.table("recordings").update(data).eq("recording_id", recording_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Recording not found")
    return response.data[0]

@router.delete("/{recording_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recording(recording_id: str):
    supabase.table("recordings").delete().eq("recording_id", recording_id).execute()
    return None

