from app.utils.database import supabase
from app import schemas
from typing import List, Optional

class RecordingTagService:
    @staticmethod
    def get_tags_by_recording_id(recording_id: str) -> List[schemas.RecordingTag]:
        response = supabase.table("recording_tags").select("*").eq("recording_id", recording_id).execute()
        return response.data

    @staticmethod
    def add_tags(recording_id: str, tags: List[str]) -> List[schemas.RecordingTag]:
        # Normalize tags
        normalized_tags = {tag.strip().lower() for tag in tags}
        
        # Get existing tags to avoid duplicates
        existing_res = supabase.table("recording_tags").select("tag").eq("recording_id", recording_id).execute()
        existing_tags = {item['tag'] for item in existing_res.data}
        
        new_tags = normalized_tags - existing_tags
        
        if not new_tags:
            return []

        rows = [{"recording_id": recording_id, "tag": t} for t in new_tags]
        response = supabase.table("recording_tags").insert(rows).execute()
        return response.data

    @staticmethod
    def delete_tag(recording_id: str, tag: str) -> None:
        tag_normalized = tag.strip().lower()
        supabase.table("recording_tags").delete().eq("recording_id", recording_id).eq("tag", tag_normalized).execute()
