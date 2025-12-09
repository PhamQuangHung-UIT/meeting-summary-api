from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from pydantic import BaseModel

from app import schemas
from app.services.recording_tag_service import RecordingTagService
from app.services.recording_service import RecordingService

router = APIRouter(prefix="/recordings", tags=["Recording Tags"])


class TagsCreateRequest(BaseModel):
    tags: List[str]


@router.get("/{recording_id}/tags", response_model=List[schemas.RecordingTag])
def get_recording_tags(recording_id: str):
    """Get all tags for a specific recording"""
    # Verify recording exists
    recording = RecordingService.get_recording_by_id(recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    return RecordingTagService.get_tags_by_recording_id(recording_id)


@router.post("/{recording_id}/tags", response_model=List[schemas.RecordingTag], status_code=status.HTTP_201_CREATED)
def add_recording_tags(recording_id: str, request: TagsCreateRequest):
    """Add one or multiple tags to a recording"""
    # Verify recording exists
    recording = RecordingService.get_recording_by_id(recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    if not request.tags:
        raise HTTPException(status_code=400, detail="At least one tag is required")

    # Normalize and validate tags
    normalized_tags = []
    for tag in request.tags:
        normalized = tag.strip().lower()
        if not normalized:
            continue
        if len(normalized) > 100:
            raise HTTPException(status_code=400, detail=f"Tag '{tag}' exceeds 100 characters")
        normalized_tags.append(normalized)

    if not normalized_tags:
        raise HTTPException(status_code=400, detail="No valid tags provided")

    # Add tags (service handles duplicates)
    created_tags = RecordingTagService.add_tags_to_recording(recording_id, normalized_tags)
    return created_tags


@router.delete("/{recording_id}/tags/{tag}", status_code=status.HTTP_204_NO_CONTENT)
def remove_recording_tag(recording_id: str, tag: str):
    """Remove a specific tag from a recording"""
    # Normalize tag for comparison
    normalized_tag = tag.strip().lower()

    # Find and delete the tag
    deleted = RecordingTagService.delete_tag_from_recording(recording_id, normalized_tag)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tag not found for this recording")

    return None


# Optional: Get recordings by tag
@router.get("/", response_model=List[schemas.Recording], tags=["Recordings"])
def get_recordings_by_tag(tag: Optional[str] = Query(None, description="Filter recordings by tag")):
    """Get all recordings, optionally filtered by tag"""
    if tag:
        normalized_tag = tag.strip().lower()
        return RecordingTagService.get_recordings_by_tag(normalized_tag)
    else:
        return RecordingService.get_all_recordings()


# Admin view: Get all tags
@router.get("/tags/all", response_model=List[schemas.RecordingTag], tags=["Recording Tags"])
def get_all_tags():
    """Get all tags across all recordings"""
    return RecordingTagService.get_all_recording_tags()


# Get distinct tags (for autocomplete/dropdown)
@router.get("/tags/distinct", response_model=List[str], tags=["Recording Tags"])
def get_distinct_tags():
    """Get all distinct tag values for autocomplete"""
    return RecordingTagService.get_distinct_tags()