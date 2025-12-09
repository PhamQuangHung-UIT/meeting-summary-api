from app.utils.database import supabase
from app import schemas
from typing import List, Optional
from app.services.audit_log_service import AuditLogService


class MarkerService:
    @staticmethod
    def get_all_markers() -> List[schemas.Marker]:
        response = supabase.table("markers").select("*").execute()
        return response.data

    @staticmethod
    def get_markers_by_recording_id(recording_id: str) -> List[schemas.Marker]:
        """Get all markers for a specific recording, ordered by time"""
        response = supabase.table("markers").select("*").eq("recording_id", recording_id).order(
            "time_seconds").execute()
        return response.data

    @staticmethod
    def get_marker_by_id(marker_id: str) -> Optional[schemas.Marker]:
        response = supabase.table("markers").select("*").eq("marker_id", marker_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def create_marker(marker: schemas.MarkerCreate) -> schemas.Marker:
        data = marker.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("markers").insert(data).execute()

        # Create audit log
        try:
            audit_log = schemas.AuditLogCreate(
                action_type="CREATE_MARKER",
                resource_type="MARKER",
                resource_id=response.data[0]['marker_id'],
                status=schemas.AuditStatus.SUCCESS,
                details=f"Created marker at {marker.time_seconds}s for recording {marker.recording_id}"
            )
            AuditLogService.create_audit_log(audit_log)
        except Exception as e:
            print(f"Error creating audit log: {e}")

        return response.data[0]

    @staticmethod
    def update_marker(marker_id: str, marker: schemas.MarkerUpdate) -> Optional[schemas.Marker]:
        data = marker.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("markers").update(data).eq("marker_id", marker_id).execute()

        if response.data:
            # Create audit log
            try:
                audit_log = schemas.AuditLogCreate(
                    action_type="UPDATE_MARKER",
                    resource_type="MARKER",
                    resource_id=marker_id,
                    status=schemas.AuditStatus.SUCCESS,
                    details=f"Updated marker {marker_id}"
                )
                AuditLogService.create_audit_log(audit_log)
            except Exception as e:
                print(f"Error creating audit log: {e}")

            return response.data[0]
        return None

    @staticmethod
    def delete_marker(marker_id: str) -> None:
        supabase.table("markers").delete().eq("marker_id", marker_id).execute()

        # Create audit log
        try:
            audit_log = schemas.AuditLogCreate(
                action_type="DELETE_MARKER",
                resource_type="MARKER",
                resource_id=marker_id,
                status=schemas.AuditStatus.SUCCESS,
                details=f"Deleted marker {marker_id}"
            )
            AuditLogService.create_audit_log(audit_log)
        except Exception as e:
            print(f"Error creating audit log: {e}")