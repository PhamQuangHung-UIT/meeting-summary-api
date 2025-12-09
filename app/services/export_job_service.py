from app.utils.database import supabase
from app import schemas
from typing import List, Optional
from app.services.audit_log_service import AuditLogService


class ExportJobService:
    @staticmethod
    def get_all_export_jobs(
            user_id: Optional[str] = None,
            recording_id: Optional[str] = None,
            status: Optional[str] = None
    ) -> List[schemas.ExportJob]:
        """Get all export jobs with optional filters"""
        query = supabase.table("export_jobs").select("*")

        if user_id:
            query = query.eq("user_id", user_id)
        if recording_id:
            query = query.eq("recording_id", recording_id)
        if status:
            query = query.eq("status", status)

        response = query.order("created_at", desc=True).execute()
        return response.data

    @staticmethod
    def get_export_job_by_id(export_id: str) -> Optional[schemas.ExportJob]:
        response = supabase.table("export_jobs").select("*").eq("export_id", export_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def create_export_job(job: schemas.ExportJobCreate) -> schemas.ExportJob:
        data = job.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("export_jobs").insert(data).execute()

        # Create audit log
        try:
            audit_log = schemas.AuditLogCreate(
                user_id=job.user_id,
                action_type="CREATE_EXPORT",
                resource_type="EXPORT_JOB",
                resource_id=response.data[0]['export_id'],
                status=schemas.AuditStatus.SUCCESS,
                details=f"Created export job for recording {job.recording_id} with type {job.export_type}"
            )
            AuditLogService.create_audit_log(audit_log)
        except Exception as e:
            print(f"Error creating audit log: {e}")

        return response.data[0]

    @staticmethod
    def update_export_job(export_id: str, job: schemas.ExportJobUpdate) -> Optional[schemas.ExportJob]:
        data = job.model_dump(mode='json', exclude_unset=True)

        # If status is being set to DONE, automatically set completed_at
        if data.get('status') == 'DONE' and 'completed_at' not in data:
            from datetime import datetime
            data['completed_at'] = datetime.utcnow().isoformat()

        response = supabase.table("export_jobs").update(data).eq("export_id", export_id).execute()

        if response.data:
            # Create audit log for status changes
            try:
                existing_job = ExportJobService.get_export_job_by_id(export_id)
                if existing_job:
                    audit_status = schemas.AuditStatus.SUCCESS if data.get(
                        'status') == 'DONE' else schemas.AuditStatus.FAILED
                    audit_log = schemas.AuditLogCreate(
                        user_id=existing_job['user_id'],
                        action_type="UPDATE_EXPORT",
                        resource_type="EXPORT_JOB",
                        resource_id=export_id,
                        status=audit_status,
                        details=f"Updated export job to status: {data.get('status', 'unknown')}"
                    )
                    AuditLogService.create_audit_log(audit_log)
            except Exception as e:
                print(f"Error creating audit log: {e}")

            return response.data[0]
        return None

    @staticmethod
    def delete_export_job(export_id: str) -> None:
        # Get job info before deleting
        job = ExportJobService.get_export_job_by_id(export_id)

        # Delete the file from storage if it exists
        if job and job.get('file_path'):
            try:
                supabase.storage.from_("exports").remove([job['file_path']])
            except Exception as e:
                print(f"Error deleting export file: {e}")

        supabase.table("export_jobs").delete().eq("export_id", export_id).execute()

        # Create audit log
        if job:
            try:
                audit_log = schemas.AuditLogCreate(
                    user_id=job['user_id'],
                    action_type="DELETE_EXPORT",
                    resource_type="EXPORT_JOB",
                    resource_id=export_id,
                    status=schemas.AuditStatus.SUCCESS,
                    details=f"Deleted export job {export_id}"
                )
                AuditLogService.create_audit_log(audit_log)
            except Exception as e:
                print(f"Error creating audit log: {e}")