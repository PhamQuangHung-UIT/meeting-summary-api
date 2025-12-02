from fastapi import APIRouter, HTTPException, status
from typing import List

from app.utils.database import supabase
from app import schemas

router = APIRouter(prefix="/transcripts", tags=["Transcript Segments"])

@router.get("/{transcript_id}/segments", response_model=List[schemas.TranscriptSegment])
def get_transcript_segments(transcript_id: str):
    response = supabase.table("transcript_segments").select("*").eq("transcript_id", transcript_id).order("start_time").execute()
    return response.data

@router.post("/{transcript_id}/segments", response_model=schemas.TranscriptSegment, status_code=status.HTTP_201_CREATED)
def create_transcript_segment(transcript_id: str, segment: schemas.TranscriptSegmentCreate):
    data = segment.model_dump(exclude_unset=True)
    data["transcript_id"] = transcript_id
    response = supabase.table("transcript_segments").insert(data).execute()
    return response.data[0]

@router.put("/segments/{segment_id}", response_model=schemas.TranscriptSegment)
def update_transcript_segment(segment_id: int, segment: schemas.TranscriptSegmentUpdate):
    response = supabase.table("transcript_segments").update(segment.model_dump(exclude_unset=True)).eq("segment_id", segment_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Segment not found")
    return response.data[0]

@router.delete("/segments/{segment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transcript_segment(segment_id: int):
    supabase.table("transcript_segments").delete().eq("segment_id", segment_id).execute()
    return None
