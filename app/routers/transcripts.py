from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID
from app.utils.database import supabase
from app import schemas

router = APIRouter(prefix="/transcripts", tags=["Transcripts"])

@router.get("/", response_model=List[schemas.Transcript])
def get_all_transcripts():
    response = supabase.table("transcripts").select("*").execute()
    return response.data

@router.get("/{transcript_id}", response_model=schemas.Transcript)
def get_transcript(transcript_id: UUID):
    response = supabase.table("transcripts").select("*").eq("transcript_id", str(transcript_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Transcript not found")
    return response.data[0]

@router.post("/", response_model=schemas.Transcript, status_code=status.HTTP_201_CREATED)
def create_transcript(transcript: schemas.TranscriptCreate):
    data = transcript.model_dump(exclude_unset=True)
    if data.get('recording_id'): data['recording_id'] = str(data['recording_id'])

    response = supabase.table("transcripts").insert(data).execute()
    return response.data[0]

@router.put("/{transcript_id}", response_model=schemas.Transcript)
def update_transcript(transcript_id: UUID, transcript: schemas.TranscriptUpdate):
    response = supabase.table("transcripts").update(transcript.model_dump(exclude_unset=True)).eq("transcript_id", str(transcript_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Transcript not found")
    return response.data[0]

@router.delete("/{transcript_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transcript(transcript_id: UUID):
    supabase.table("transcripts").delete().eq("transcript_id", str(transcript_id)).execute()
    return None
