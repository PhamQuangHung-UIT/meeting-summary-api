from fastapi import APIRouter, HTTPException, status
from typing import List
from app.utils.database import supabase
from app import schemas

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])

@router.get("/", response_model=List[schemas.AuditLog])
def get_all_audit_logs():
    response = supabase.table("audit_logs").select("*").execute()
    return response.data

@router.get("/{log_id}", response_model=schemas.AuditLog)
def get_audit_log(log_id: int):
    response = supabase.table("audit_logs").select("*").eq("log_id", log_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return response.data[0]

@router.post("/", response_model=schemas.AuditLog, status_code=status.HTTP_201_CREATED)
def create_audit_log(log: schemas.AuditLogCreate):
    data = log.model_dump(exclude_unset=True)

        
    response = supabase.table("audit_logs").insert(data).execute()
    return response.data[0]

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_audit_log(log_id: int):
    supabase.table("audit_logs").delete().eq("log_id", log_id).execute()
    return None
