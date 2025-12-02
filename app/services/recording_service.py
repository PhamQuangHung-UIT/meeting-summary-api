from app.utils.database import supabase
from app import schemas
from typing import List, Optional

class RecordingService:
    @staticmethod
    def get_all_recordings() -> List[schemas.Recording]:
        response = supabase.table("recordings").select("*").execute()
        return response.data

    @staticmethod
    def get_recording_by_id(recording_id: str) -> Optional[schemas.Recording]:
        response = supabase.table("recordings").select("*").eq("recording_id", recording_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def create_recording(recording: schemas.RecordingCreate) -> schemas.Recording:
        data = recording.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("recordings").insert(data).execute()
        return response.data[0]

    @staticmethod
    def update_recording(recording_id: str, recording: schemas.RecordingUpdate) -> Optional[schemas.Recording]:
        data = recording.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("recordings").update(data).eq("recording_id", recording_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def delete_recording(recording_id: str) -> None:
        supabase.table("recordings").delete().eq("recording_id", recording_id).execute()
