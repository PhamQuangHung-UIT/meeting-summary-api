from fastapi import APIRouter, HTTPException, status
from typing import List

from app.utils.database import supabase
from app import schemas

router = APIRouter(prefix="/markers", tags=["Markers"])

@router.get("/", response_model=List[schemas.Marker])
def get_all_markers():
    response = supabase.table("markers").select("*").execute()
    return response.data

@router.get("/{marker_id}", response_model=schemas.Marker)
def get_marker(marker_id: str):
    response = supabase.table("markers").select("*").eq("marker_id", marker_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Marker not found")
    return response.data[0]

@router.post("/", response_model=schemas.Marker, status_code=status.HTTP_201_CREATED)
def create_marker(marker: schemas.MarkerCreate):
    data = marker.model_dump(mode='json', exclude_unset=True)
    response = supabase.table("markers").insert(data).execute()
    return response.data[0]

@router.put("/{marker_id}", response_model=schemas.Marker)
def update_marker(marker_id: str, marker: schemas.MarkerUpdate):
    data = marker.model_dump(mode='json', exclude_unset=True)
    response = supabase.table("markers").update(data).eq("marker_id", marker_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Marker not found")
    return response.data[0]

@router.delete("/{marker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_marker(marker_id: str):
    supabase.table("markers").delete().eq("marker_id", marker_id).execute()
    return None
