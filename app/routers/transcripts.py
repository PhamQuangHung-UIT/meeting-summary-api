from fastapi import APIRouter, HTTPException, status
from typing import List

from app import schemas
from app.services.transcript_service import TranscriptService

router = APIRouter(prefix="/transcripts", tags=["Transcripts"])

@router.get("/", response_model=List[schemas.Transcript])
def get_all_transcripts():
    return TranscriptService.get_all_transcripts()

@router.get("/{transcript_id}", response_model=schemas.Transcript)
def get_transcript(transcript_id: str):
    transcript = TranscriptService.get_transcript_by_id(transcript_id)
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    return transcript

@router.post("/", response_model=schemas.Transcript, status_code=status.HTTP_201_CREATED)
def create_transcript(transcript: schemas.TranscriptCreate):
    return TranscriptService.create_transcript(transcript)

@router.put("/{transcript_id}", response_model=schemas.Transcript)
def update_transcript(transcript_id: str, transcript: schemas.TranscriptUpdate):
    updated_transcript = TranscriptService.update_transcript(transcript_id, transcript)
    if not updated_transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    return updated_transcript

@router.delete("/{transcript_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transcript(transcript_id: str):
    TranscriptService.delete_transcript(transcript_id)
    return None

