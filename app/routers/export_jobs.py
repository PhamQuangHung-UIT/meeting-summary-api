from fastapi import APIRouter, HTTPException, status
from typing import List

from app import schemas
from app.services.export_job_service import ExportJobService

router = APIRouter(prefix="/export_jobs", tags=["Export Jobs"])

@router.get("/{export_id}", response_model=schemas.ExportJob)
def get_export_job(export_id: str):
    job = ExportJobService.get_export_job_by_id(export_id)
    if not job:
        raise HTTPException(status_code=404, detail="Export Job not found")
    return job

@router.put("/{export_id}", response_model=schemas.ExportJob)
def update_export_job(export_id: str, job: schemas.ExportJobUpdate):
    updated_job = ExportJobService.update_export_job(export_id, job)
    if not updated_job:
        raise HTTPException(status_code=404, detail="Export Job not found")
    return updated_job

@router.delete("/{export_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_export_job(export_id: str):
    ExportJobService.delete_export_job(export_id)
    return None
