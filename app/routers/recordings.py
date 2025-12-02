from fastapi import APIRouter, HTTPException, status
from typing import List

from app import schemas
from app.services.recording_service import RecordingService
from app.services.transcript_service import TranscriptService

router = APIRouter(prefix="/recordings", tags=["Recordings"])

@router.get("/", response_model=List[schemas.Recording])
def get_all_recordings():
    return RecordingService.get_all_recordings()

@router.get("/{recording_id}", response_model=schemas.Recording)
def get_recording(recording_id: str):
    recording = RecordingService.get_recording_by_id(recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    return recording

@router.post("/", response_model=schemas.Recording, status_code=status.HTTP_201_CREATED)
def create_recording(recording: schemas.RecordingCreate):
    return RecordingService.create_recording(recording)

@router.put("/{recording_id}", response_model=schemas.Recording)
def update_recording(recording_id: str, recording: schemas.RecordingUpdate):
    updated_recording = RecordingService.update_recording(recording_id, recording)
    if not updated_recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    return updated_recording

@router.delete("/{recording_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recording(recording_id: str):
    RecordingService.delete_recording(recording_id)
    return None

@router.post("/{recording_id}/transcribe", response_model=schemas.Transcript)
def transcribe_recording(recording_id: str):
    try:
        transcript = RecordingService.transcribe_recording(recording_id)
        if not transcript:
             raise HTTPException(status_code=404, detail="Recording not found")
        return transcript
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{recording_id}/transcripts", response_model=List[schemas.Transcript])
def get_recording_transcripts(recording_id: str, latest: bool = False):
    return TranscriptService.get_transcripts_by_recording_id(recording_id, latest)

