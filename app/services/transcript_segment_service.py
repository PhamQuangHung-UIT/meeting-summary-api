from app.utils.database import supabase
from app import schemas
from typing import List, Optional

class TranscriptSegmentService:
    @staticmethod
    def get_segments_by_transcript_id(transcript_id: str) -> List[schemas.TranscriptSegment]:
        response = supabase.table("transcript_segments").select("*").eq("transcript_id", transcript_id).order("start_time").execute()
        return response.data

    @staticmethod
    def create_transcript_segment(transcript_id: str, segment: schemas.TranscriptSegmentCreate) -> schemas.TranscriptSegment:
        data = segment.model_dump(mode='json', exclude_unset=True)
        data["transcript_id"] = transcript_id
        response = supabase.table("transcript_segments").insert(data).execute()
        return response.data[0]

    @staticmethod
    def update_transcript_segment(transcript_id: str, segment_id: int, segment: schemas.TranscriptSegmentUpdate) -> Optional[schemas.TranscriptSegment]:
        data = segment.model_dump(mode='json', exclude_unset=True)
        response = supabase.table("transcript_segments").update(data).eq("transcript_id", transcript_id).eq("segment_id", segment_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def delete_transcript_segment(transcript_id: str, segment_id: int) -> None:
        supabase.table("transcript_segments").delete().eq("transcript_id", transcript_id).eq("segment_id", segment_id).execute()
