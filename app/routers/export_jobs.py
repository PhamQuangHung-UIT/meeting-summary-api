from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from pydantic import BaseModel

from app import schemas
from app.services.export_job_service import ExportJobService

router = APIRouter(tags=["Export Jobs"])


class ExportCreateRequest(BaseModel):
    export_type: str  # e.g., "TRANSCRIPT_PDF", "SUMMARY_DOCX", "FULL_ZIP"


# POST /recordings/:id/export - Create export job for a recording
@router.post("/recordings/{recording_id}/export", response_model=schemas.ExportJob, status_code=status.HTTP_201_CREATED)
def create_recording_export(recording_id: str, request: ExportCreateRequest):
    """Create an export job for a recording"""
    from app.services.recording_service import RecordingService

    # Validate recording exists
    recording = RecordingService.get_recording_by_id(recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    # Validate export type
    valid_types = ["TRANSCRIPT_PDF", "TRANSCRIPT_DOCX", "SUMMARY_PDF", "SUMMARY_DOCX", "FULL_ZIP"]
    if request.export_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid export type. Must be one of: {', '.join(valid_types)}"
        )

    # Create export job
    export_job_create = schemas.ExportJobCreate(
        user_id=recording['user_id'],
        recording_id=recording_id,
        export_type=request.export_type,
        status=schemas.ExportStatus.PENDING
    )

    export_job = ExportJobService.create_export_job(export_job_create)

    # TODO: Trigger background worker/edge function to process the export
    # This would typically be done via a task queue (Celery, Redis Queue, etc.)
    # or by triggering a Supabase Edge Function
    # For now, the job is created with PENDING status

    return export_job


# GET /export-jobs/:id - Get export job status
@router.get("/export-jobs/{export_id}", response_model=schemas.ExportJob)
def get_export_job_status(export_id: str):
    """Get the status of an export job, with download link if completed"""
    job = ExportJobService.get_export_job_by_id(export_id)
    if not job:
        raise HTTPException(status_code=404, detail="Export Job not found")

    # If job is DONE and has a file_path, generate signed URL
    if job['status'] == 'DONE' and job.get('file_path'):
        from app.utils.database import supabase
        try:
            # Generate signed URL valid for 1 hour
            signed_url = supabase.storage.from_("exports").create_signed_url(
                job['file_path'],
                3600  # 1 hour
            )
            job['download_url'] = signed_url['signedURL']
        except Exception as e:
            print(f"Error generating signed URL: {e}")

    return job


# Legacy endpoints for backward compatibility
@router.get("/export_jobs", response_model=List[schemas.ExportJob])
def get_all_export_jobs(
        user_id: Optional[str] = Query(None, description="Filter by user ID"),
        recording_id: Optional[str] = Query(None, description="Filter by recording ID"),
        status: Optional[str] = Query(None, description="Filter by status")
):
    """Get all export jobs with optional filters"""
    return ExportJobService.get_all_export_jobs(
        user_id=user_id,
        recording_id=recording_id,
        status=status
    )


@router.get("/export_jobs/{export_id}", response_model=schemas.ExportJob)
def get_export_job(export_id: str):
    """Legacy endpoint - use /export-jobs/:id instead"""
    job = ExportJobService.get_export_job_by_id(export_id)
    if not job:
        raise HTTPException(status_code=404, detail="Export Job not found")
    return job


@router.post("/export_jobs", response_model=schemas.ExportJob, status_code=status.HTTP_201_CREATED)
def create_export_job_direct(job: schemas.ExportJobCreate):
    """Create export job directly (legacy endpoint)"""
    return ExportJobService.create_export_job(job)


@router.put("/export_jobs/{export_id}", response_model=schemas.ExportJob)
def update_export_job(export_id: str, job: schemas.ExportJobUpdate):
    """Update export job status (used by background workers)"""
    updated_job = ExportJobService.update_export_job(export_id, job)
    if not updated_job:
        raise HTTPException(status_code=404, detail="Export Job not found")
    return updated_job


@router.delete("/export_jobs/{export_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_export_job(export_id: str):
    """Delete an export job"""
    ExportJobService.delete_export_job(export_id)
    return None