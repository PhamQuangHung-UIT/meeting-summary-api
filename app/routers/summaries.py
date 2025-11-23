from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID
from app.utils.database import supabase
from app import schemas

router = APIRouter(prefix="/summaries", tags=["Summaries"])

@router.get("/", response_model=List[schemas.Summary])
def get_all_summaries():
    response = supabase.table("summaries").select("*").execute()
    return response.data

@router.get("/{summary_id}", response_model=schemas.Summary)
def get_summary(summary_id: UUID):
    response = supabase.table("summaries").select("*").eq("summary_id", str(summary_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Summary not found")
    return response.data[0]

@router.post("/", response_model=schemas.Summary, status_code=status.HTTP_201_CREATED)
def create_summary(summary: schemas.SummaryCreate):
    data = summary.model_dump(exclude_unset=True)
    if data.get('recording_id'): data['recording_id'] = str(data['recording_id'])

    response = supabase.table("summaries").insert(data).execute()
    return response.data[0]

@router.put("/{summary_id}", response_model=schemas.Summary)
def update_summary(summary_id: UUID, summary: schemas.SummaryUpdate):
    response = supabase.table("summaries").update(summary.model_dump(exclude_unset=True)).eq("summary_id", str(summary_id)).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Summary not found")
    return response.data[0]

@router.delete("/{summary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_summary(summary_id: UUID):
    supabase.table("summaries").delete().eq("summary_id", str(summary_id)).execute()
    return None
