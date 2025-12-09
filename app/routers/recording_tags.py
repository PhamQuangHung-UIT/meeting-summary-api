from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from pydantic import BaseModel

from app import schemas
from app.services.recording_tag_service import RecordingTagService

router = APIRouter(prefix="/recordings", tags=["Recording Tags"])


class TagsCreateRequest(BaseModel):
    tags: List[str]  # Support multiple tags at once


# POST /recordings/:id/tags - Add one or multiple tags
@router.post("/{recording_id}/tags", response_model=List[schemas.RecordingTag], status_code=status.HTTP_201_CREATED)
def add_recording_tags(recording_id: str, request: TagsCreateRequest):
    """Add one or multiple tags to a recording"""
    from app.services.recording_service import RecordingService

    # Check if recording exists
    recording = RecordingService.get_recording_by_id(recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    # Get existing tags for this recording to avoid duplicates
    existing_tags = RecordingTagService.get_tags_by_recording_id(recording_id)
    existing_tag_values = {tag['tag'].lower().strip() for tag in existing_tags}

    created_tags = []
    for tag_value in request.tags:
        # Normalize: lowercase and trim
        normalized_tag = tag_value.lower().strip()

        # Skip if tag already exists
        if normalized_tag in existing_tag_values:
            continue

        tag_create = schemas.RecordingTagCreate(
            recording_id=recording_id,
            tag=normalized_tag
        )
        created_tag = RecordingTagService.create_recording_tag(tag_create)
        created_tags.append(created_tag)

    return created_tags


# GET /recordings/:id/tags - Get all tags for a recording
@router.get("/{recording_id}/tags", response_model=List[schemas.RecordingTag])
def get_recording_tags(recording_id: str):
    """Get all tags for a specific recording"""
    return RecordingTagService.get_tags_by_recording_id(recording_id)


# DELETE /recordings/:id/tags/:tag - Remove a specific tag
@router.delete("/{recording_id}/tags/{tag}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recording_tag(recording_id: str, tag: str):
    """Delete a specific tag from a recording"""
    # Normalize tag for comparison
    normalized_tag = tag.lower().strip()

    # Find the tag
    tags = RecordingTagService.get_tags_by_recording_id(recording_id)
    matching_tag = None
    for t in tags:
        if t['tag'].lower().strip() == normalized_tag:
            matching_tag = t
            break

    if not matching_tag:
        raise HTTPException(status_code=404, detail="Tag not found for this recording")

    RecordingTagService.delete_recording_tag(matching_tag['id'])
    return None


# Also keep old endpoints for backward compatibility
@router.get("/tags", response_model=List[schemas.RecordingTag])
def get_all_recording_tags():
    """Get all recording tags (legacy endpoint)"""
    return RecordingTagService.get_all_recording_tags()


@router.get("/tags/{id}", response_model=schemas.RecordingTag)
def get_recording_tag(id: str):
    """Get a specific recording tag by ID (legacy endpoint)"""
    tag = RecordingTagService.get_recording_tag_by_id(id)
    if not tag:
        raise HTTPException(status_code=404, detail="Recording Tag not found")
    return tag


@router.post("/tags", response_model=schemas.RecordingTag, status_code=status.HTTP_201_CREATED)
def create_recording_tag_direct(tag: schemas.RecordingTagCreate):
    """Create a recording tag directly (legacy endpoint)"""
    return RecordingTagService.create_recording_tag(tag)


@router.delete("/tags/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recording_tag_direct(id: str):
    """Delete a recording tag by ID (legacy endpoint)"""
    RecordingTagService.delete_recording_tag(id)
    return None