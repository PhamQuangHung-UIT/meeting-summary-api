from app.utils.database import supabase
from app import schemas
from typing import List, Optional

class TranscriptService:
    @staticmethod
    def get_all_transcripts() -> List[schemas.Transcript]:
        response = supabase.table("transcripts").select("*").execute()
        return response.data

    @staticmethod
    def get_transcript_by_id(transcript_id: str) -> Optional[schemas.Transcript]:
        response = supabase.table("transcripts").select("*").eq("transcript_id", transcript_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def create_transcript(transcript: schemas.TranscriptCreate) -> schemas.Transcript:
        data = transcript.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("transcripts").insert(data).execute()
        return response.data[0]

    @staticmethod
    def update_transcript(transcript_id: str, transcript: schemas.TranscriptUpdate) -> Optional[schemas.Transcript]:
        data = transcript.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("transcripts").update(data).eq("transcript_id", transcript_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def delete_transcript(transcript_id: str) -> None:
        supabase.table("transcripts").delete().eq("transcript_id", transcript_id).execute()
