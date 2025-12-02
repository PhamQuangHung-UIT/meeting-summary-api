from fastapi import APIRouter, HTTPException, status
from typing import List

from app import schemas
from app.services.summary_service import SummaryService

router = APIRouter(prefix="/summaries", tags=["Summaries"])

@router.get("/", response_model=List[schemas.Summary])
def get_all_summaries():
    return SummaryService.get_all_summaries()

@router.get("/{summary_id}", response_model=schemas.Summary)
def get_summary(summary_id: str):
    summary = SummaryService.get_summary_by_id(summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary

@router.post("/", response_model=schemas.Summary, status_code=status.HTTP_201_CREATED)
def create_summary(summary: schemas.SummaryCreate):
    return SummaryService.create_summary(summary)

@router.put("/{summary_id}", response_model=schemas.Summary)
def update_summary(summary_id: str, summary: schemas.SummaryUpdate):
    updated_summary = SummaryService.update_summary(summary_id, summary)
    if not updated_summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return updated_summary

@router.delete("/{summary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_summary(summary_id: str):
    SummaryService.delete_summary(summary_id)
    return None
