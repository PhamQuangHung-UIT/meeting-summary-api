from app.utils.database import supabase
from app import schemas
from typing import List, Optional
from app.services.audit_log_service import AuditLogService


class RecordingTagService:
    @staticmethod
    def get_all_recording_tags() -> List[schemas.RecordingTag]:
        response = supabase.table("recording_tags").select("*").execute()
        return response.data

    @staticmethod
    def get_tags_by_recording_id(recording_id: str) -> List[schemas.RecordingTag]:
        """Get all tags for a specific recording"""
        response = supabase.table("recording_tags").select("*").eq("recording_id", recording_id).order("tag").execute()
        return response.data

    @staticmethod
    def get_recording_tag_by_id(id: str) -> Optional[schemas.RecordingTag]:
        response = supabase.table("recording_tags").select("*").eq("id", id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def create_recording_tag(tag: schemas.RecordingTagCreate) -> schemas.RecordingTag:
        # Normalize tag: lowercase and trim
        normalized_tag = tag.tag.lower().strip()

        # Check if this exact tag already exists for this recording
        existing = supabase.table("recording_tags") \
            .select("*") \
            .eq("recording_id", tag.recording_id) \
            .ilike("tag", normalized_tag) \
            .execute()

        if existing.data:
            # Tag already exists, return the existing one
            return existing.data[0]

        # Create new tag with normalized value
        data = {
            "recording_id": tag.recording_id,
            "tag": normalized_tag
        }
        response = supabase.table("recording_tags").insert(data).execute()

        # Create audit log
        try:
            audit_log = schemas.AuditLogCreate(
                action_type="ADD_TAG",
                resource_type="RECORDING_TAG",
                resource_id=response.data[0]['id'],
                status=schemas.AuditStatus.SUCCESS,
                details=f"Added tag '{normalized_tag}' to recording {tag.recording_id}"
            )
            AuditLogService.create_audit_log(audit_log)
        except Exception as e:
            print(f"Error creating audit log: {e}")

        return response.data[0]

    @staticmethod
    def delete_recording_tag(id: str) -> None:
        # Get tag info before deleting for audit log
        tag = RecordingTagService.get_recording_tag_by_id(id)

        supabase.table("recording_tags").delete().eq("id", id).execute()

        # Create audit log
        if tag:
            try:
                audit_log = schemas.AuditLogCreate(
                    action_type="REMOVE_TAG",
                    resource_type="RECORDING_TAG",
                    resource_id=id,
                    status=schemas.AuditStatus.SUCCESS,
                    details=f"Removed tag '{tag['tag']}' from recording {tag['recording_id']}"
                )
                AuditLogService.create_audit_log(audit_log)
            except Exception as e:
                print(f"Error creating audit log: {e}")