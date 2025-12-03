from app.utils.database import supabase
from app import schemas
from app.utils import transcriber
from typing import List, Optional
import json
import os

class RecordingService:
    @staticmethod
    def get_all_recordings() -> List[schemas.Recording]:
        response = supabase.table("recordings").select("*").execute()
        return response.data

    @staticmethod
    def get_recordings_by_user_id(user_id: str) -> List[schemas.Recording]:
        response = supabase.table("recordings").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
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

    @staticmethod
    def transcribe_recording(recording_id: str) -> Optional[schemas.Transcript]:
        # 1. Fetch recording
        recording_response = supabase.table("recordings").select("*").eq("recording_id", recording_id).execute()
        if not recording_response.data:
            return None
        recording = recording_response.data[0]

        # 2. Check status
        if recording['status'] != 'PROCESSED':
            raise ValueError("Recording is not processed yet.")

        # 3. Read audio file
        file_path = recording['file_path']
        try:
            audio_bytes = supabase.storage.from_("recordings").download(file_path)
        except Exception as e:
             raise FileNotFoundError(f"Audio file not found in storage at {file_path}: {str(e)}")
        
        file_extension = file_path.split('.')[-1]

        # 4. Call transcriber
        try:
            transcript_json_str = transcriber.transcribe(audio_bytes, file_extension)
            transcript_data = json.loads(transcript_json_str)
        except Exception as e:
            raise RuntimeError(f"Transcription failed: {str(e)}")

        # 5. Determine version_no
        # Get max version_no for this recording
        transcripts_response = supabase.table("transcripts").select("version_no").eq("recording_id", recording_id).order("version_no", desc=True).limit(1).execute()
        current_version = 0
        if transcripts_response.data:
            current_version = transcripts_response.data[0]['version_no']
        new_version = current_version + 1

        # 6. Insert into TRANSCRIPTS
        supabase.table("transcripts").update({"is_active": False}).eq("recording_id", recording_id).execute()

        new_transcript_data = {
            "recording_id": recording_id,
            "version_no": new_version,
            "type": "AI_ORIGINAL",
            "language": "vi", # Default or detect? The prompt implies it handles it, but schema needs it. Let's assume 'vi' or 'en' or null.
            "is_active": True
        }
        transcript_insert_response = supabase.table("transcripts").insert(new_transcript_data).execute()
        new_transcript = transcript_insert_response.data[0]
        transcript_id = new_transcript['transcript_id']

        # 7. Insert into TRANSCRIPT_SEGMENTS
        segments_to_insert = []
        speakers_set = set()
        
        for idx, segment in enumerate(transcript_data):
            segments_to_insert.append({
                "transcript_id": transcript_id,
                "sequence": idx + 1,
                "start_time": segment['start_time'],
                "end_time": segment['end_time'],
                "content": segment['content'],
                "speaker_label": segment['speaker_label'],
                "confidence": 1.0 # Gemini doesn't return confidence per segment in this prompt yet
            })
            speakers_set.add(segment['speaker_label'])

        if segments_to_insert:
            supabase.table("transcript_segments").insert(segments_to_insert).execute()

        # 8. Insert into RECORDING_SPEAKERS
        # Check existing speakers for this recording
        existing_speakers_response = supabase.table("recording_speakers").select("speaker_label").eq("recording_id", recording_id).execute()
        existing_labels = {s['speaker_label'] for s in existing_speakers_response.data}
        
        new_speakers = []
        for label in speakers_set:
            if label not in existing_labels:
                new_speakers.append({
                    "recording_id": recording_id,
                    "speaker_label": label,
                    "display_name": label # Initial display name same as label
                })
        
        if new_speakers:
            supabase.table("recording_speakers").insert(new_speakers).execute()

        return new_transcript
