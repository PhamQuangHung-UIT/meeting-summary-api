from fastapi import APIRouter, HTTPException, status
from typing import List

from app import schemas
from app.services.recording_tag_service import RecordingTagService

router = APIRouter(prefix="/recording_tags", tags=["Recording Tags"])

@router.get("/", response_model=List[schemas.RecordingTag])
def get_all_recording_tags():
    return RecordingTagService.get_all_recording_tags()

@router.get("/{id}", response_model=schemas.RecordingTag)
def get_recording_tag(id: str):
    tag = RecordingTagService.get_recording_tag_by_id(id)
    if not tag:
        raise HTTPException(status_code=404, detail="Recording Tag not found")
    return tag

@router.post("/", response_model=schemas.RecordingTag, status_code=status.HTTP_201_CREATED)
def create_recording_tag(tag: schemas.RecordingTagCreate):
    return RecordingTagService.create_recording_tag(tag)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recording_tag(id: str):
    RecordingTagService.delete_recording_tag(id)
    return None
