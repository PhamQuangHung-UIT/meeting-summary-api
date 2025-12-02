from app.utils.database import supabase
from app import schemas
from typing import List, Optional

class ExportJobService:
    @staticmethod
    def get_all_export_jobs() -> List[schemas.ExportJob]:
        response = supabase.table("export_jobs").select("*").execute()
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
        return response.data[0]

    @staticmethod
    def update_export_job(export_id: str, job: schemas.ExportJobUpdate) -> Optional[schemas.ExportJob]:
        data = job.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("export_jobs").update(data).eq("export_id", export_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def delete_export_job(export_id: str) -> None:
        supabase.table("export_jobs").delete().eq("export_id", export_id).execute()
