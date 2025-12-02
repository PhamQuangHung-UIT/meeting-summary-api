from fastapi import APIRouter, HTTPException, status
from typing import List

from app.utils.database import supabase
from app import schemas

router = APIRouter(prefix="/recordings", tags=["Recording Speakers"])

@router.get("/{recording_id}/speakers", response_model=List[schemas.RecordingSpeaker])
def get_recording_speakers(recording_id: str):
    response = supabase.table("recording_speakers").select("*").eq("recording_id", recording_id).execute()
    return response.data

@router.post("/{recording_id}/speakers", response_model=schemas.RecordingSpeaker, status_code=status.HTTP_201_CREATED)
def create_recording_speaker(recording_id: str, speaker: schemas.RecordingSpeakerCreate):
    data = speaker.model_dump(mode='json', exclude_unset=True)
    data["recording_id"] = recording_id
    response = supabase.table("recording_speakers").insert(data).execute()
    return response.data[0]

@router.put("/speakers/{speaker_id}", response_model=schemas.RecordingSpeaker)
def update_recording_speaker(speaker_id: int, speaker: schemas.RecordingSpeakerUpdate):
    response = supabase.table("recording_speakers").update(speaker.model_dump(mode='json', exclude_unset=True)).eq("id", speaker_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Speaker not found")
    return response.data[0]

@router.delete("/speakers/{speaker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recording_speaker(speaker_id: int):
    supabase.table("recording_speakers").delete().eq("id", speaker_id).execute()
    return None
