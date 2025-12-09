from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from app import schemas
from app.services.marker_service import MarkerService

router = APIRouter(prefix="/recordings", tags=["Markers"])


# GET /recordings/:id/markers
@router.get("/{recording_id}/markers", response_model=List[schemas.Marker])
def get_recording_markers(recording_id: str):
    """Get all markers for a specific recording"""
    return MarkerService.get_markers_by_recording_id(recording_id)


# POST /recordings/:id/markers
@router.post("/{recording_id}/markers", response_model=schemas.Marker, status_code=status.HTTP_201_CREATED)
def create_recording_marker(recording_id: str, marker: schemas.MarkerCreate):
    """Create a new marker for a recording"""
    # Validate that time_seconds doesn't exceed recording duration
    from app.services.recording_service import RecordingService
    recording = RecordingService.get_recording_by_id(recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    if marker.time_seconds > recording['duration_seconds']:
        raise HTTPException(
            status_code=400,
            detail=f"Marker time ({marker.time_seconds}s) exceeds recording duration ({recording['duration_seconds']}s)"
        )

    # Ensure recording_id matches
    marker_data = marker.model_copy()
    marker_data.recording_id = recording_id

    return MarkerService.create_marker(marker_data)


# PATCH /markers/:id
@router.patch("/markers/{marker_id}", response_model=schemas.Marker)
def update_marker(marker_id: str, marker_update: schemas.MarkerUpdate):
    """Update a marker"""
    # If time_seconds is being updated, validate against recording duration
    if marker_update.time_seconds is not None:
        existing_marker = MarkerService.get_marker_by_id(marker_id)
        if not existing_marker:
            raise HTTPException(status_code=404, detail="Marker not found")

        from app.services.recording_service import RecordingService
        recording = RecordingService.get_recording_by_id(existing_marker['recording_id'])

        if marker_update.time_seconds > recording['duration_seconds']:
            raise HTTPException(
                status_code=400,
                detail=f"Marker time ({marker_update.time_seconds}s) exceeds recording duration ({recording['duration_seconds']}s)"
            )

    updated_marker = MarkerService.update_marker(marker_id, marker_update)
    if not updated_marker:
        raise HTTPException(status_code=404, detail="Marker not found")
    return updated_marker


# DELETE /markers/:id
@router.delete("/markers/{marker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_marker(marker_id: str):
    """Delete a marker"""
    existing_marker = MarkerService.get_marker_by_id(marker_id)
    if not existing_marker:
        raise HTTPException(status_code=404, detail="Marker not found")

    MarkerService.delete_marker(marker_id)
    return None