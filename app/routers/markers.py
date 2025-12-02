from fastapi import APIRouter, HTTPException, status
from typing import List

from app import schemas
from app.services.marker_service import MarkerService

router = APIRouter(prefix="/markers", tags=["Markers"])

@router.get("/", response_model=List[schemas.Marker])
def get_all_markers():
    return MarkerService.get_all_markers()

@router.get("/{marker_id}", response_model=schemas.Marker)
def get_marker(marker_id: str):
    marker = MarkerService.get_marker_by_id(marker_id)
    if not marker:
        raise HTTPException(status_code=404, detail="Marker not found")
    return marker

@router.post("/", response_model=schemas.Marker, status_code=status.HTTP_201_CREATED)
def create_marker(marker: schemas.MarkerCreate):
    return MarkerService.create_marker(marker)

@router.put("/{marker_id}", response_model=schemas.Marker)
def update_marker(marker_id: str, marker: schemas.MarkerUpdate):
    updated_marker = MarkerService.update_marker(marker_id, marker)
    if not updated_marker:
        raise HTTPException(status_code=404, detail="Marker not found")
    return updated_marker

@router.delete("/{marker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_marker(marker_id: str):
    MarkerService.delete_marker(marker_id)
    return None
