from app.utils.database import supabase
from app import schemas
from typing import List, Optional

class RecordingTagService:
    @staticmethod
    def get_all_recording_tags() -> List[schemas.RecordingTag]:
        response = supabase.table("recording_tags").select("*").execute()
        return response.data

    @staticmethod
    def get_recording_tag_by_id(id: str) -> Optional[schemas.RecordingTag]:
        response = supabase.table("recording_tags").select("*").eq("id", id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def create_recording_tag(tag: schemas.RecordingTagCreate) -> schemas.RecordingTag:
        data = tag.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("recording_tags").insert(data).execute()
        return response.data[0]

    @staticmethod
    def delete_recording_tag(id: str) -> None:
        supabase.table("recording_tags").delete().eq("id", id).execute()
