from app.utils.database import supabase
from typing import Optional

def create_audit_log(
    user_id: Optional[str],
    action_type: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    status: str = "SUCCESS",
    details: Optional[str] = None,
    error_code: Optional[str] = None,
    ip_address: Optional[str] = None
) -> None:
    """
    Creates an entry in the AUDIT_LOGS table.
    """
    data = {
        "user_id": user_id,
        "action_type": action_type,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "status": status,
        "details": details,
        "error_code": error_code,
        "ip_address": ip_address
    }
    
    try:
        supabase.table("audit_logs").insert(data).execute()
    except Exception as e:
        # We generally don't want audit logging failure to crash the main request,
        # but we should log it to stderr/stdout
        print(f"Failed to create audit log: {e}")
