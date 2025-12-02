from app.utils.database import supabase
from app import schemas
from typing import List, Optional

class SummaryService:
    @staticmethod
    def get_all_summaries() -> List[schemas.Summary]:
        response = supabase.table("summaries").select("*").execute()
        return response.data

    @staticmethod
    def get_summary_by_id(summary_id: str) -> Optional[schemas.Summary]:
        response = supabase.table("summaries").select("*").eq("summary_id", summary_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def create_summary(summary: schemas.SummaryCreate) -> schemas.Summary:
        data = summary.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("summaries").insert(data).execute()
        return response.data[0]

    @staticmethod
    def update_summary(summary_id: str, summary: schemas.SummaryUpdate) -> Optional[schemas.Summary]:
        data = summary.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("summaries").update(data).eq("summary_id", summary_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def delete_summary(summary_id: str) -> None:
        supabase.table("summaries").delete().eq("summary_id", summary_id).execute()
