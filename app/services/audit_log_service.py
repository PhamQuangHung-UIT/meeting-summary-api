from app.utils.database import supabase
from app import schemas
from typing import List, Optional

class AuditLogService:
    @staticmethod
    def get_all_audit_logs() -> List[schemas.AuditLog]:
        response = supabase.table("audit_logs").select("*").execute()
        return response.data

    @staticmethod
    def get_audit_log_by_id(log_id: int) -> Optional[schemas.AuditLog]:
        response = supabase.table("audit_logs").select("*").eq("log_id", log_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def create_audit_log(log: schemas.AuditLogCreate) -> schemas.AuditLog:
        data = log.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("audit_logs").insert(data).execute()
        return response.data[0]

    @staticmethod
    def delete_audit_log(log_id: int) -> None:
        supabase.table("audit_logs").delete().eq("log_id", log_id).execute()
