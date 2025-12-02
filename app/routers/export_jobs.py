from fastapi import APIRouter, HTTPException, status
from typing import List

from app.utils.database import supabase
from app import schemas

router = APIRouter(prefix="/export_jobs", tags=["Export Jobs"])

@router.get("/", response_model=List[schemas.ExportJob])
def get_all_export_jobs():
    response = supabase.table("export_jobs").select("*").execute()
    return response.data

@router.get("/{export_id}", response_model=schemas.ExportJob)
def get_export_job(export_id: str):
    response = supabase.table("export_jobs").select("*").eq("export_id", export_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Export Job not found")
    return response.data[0]

@router.post("/", response_model=schemas.ExportJob, status_code=status.HTTP_201_CREATED)
def create_export_job(job: schemas.ExportJobCreate):
    data = job.model_dump(mode='json', exclude_unset=True)
    response = supabase.table("export_jobs").insert(data).execute()
    return response.data[0]

@router.put("/{export_id}", response_model=schemas.ExportJob)
def update_export_job(export_id: str, job: schemas.ExportJobUpdate):
    data = job.model_dump(mode='json', exclude_unset=True)
    response = supabase.table("export_jobs").update(data).eq("export_id", export_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Export Job not found")
    return response.data[0]

@router.delete("/{export_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_export_job(export_id: str):
    supabase.table("export_jobs").delete().eq("export_id", export_id).execute()
    return None
