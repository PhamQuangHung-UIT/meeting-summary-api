from app.utils.database import supabase
from app import schemas
from typing import List, Optional

class MarkerService:
    @staticmethod
    def get_all_markers() -> List[schemas.Marker]:
        response = supabase.table("markers").select("*").execute()
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
        return response.data[0]

    @staticmethod
    def update_marker(marker_id: str, marker: schemas.MarkerUpdate) -> Optional[schemas.Marker]:
        data = marker.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("markers").update(data).eq("marker_id", marker_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def delete_marker(marker_id: str) -> None:
        supabase.table("markers").delete().eq("marker_id", marker_id).execute()
