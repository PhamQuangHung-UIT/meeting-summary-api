from typing import List, Dict, Any

def clean_transcript_for_summary(segments: List[Dict[str, Any]]) -> str:
    """
    Prepares transcript content for summarization by removing timestamps and joining text.
    
    Args:
        segments: List of transcript segment dictionaries
        
    Returns:
        String containing the cleaned transcript text with speaker labels
    """
    cleaned_text = []
    for segment in segments:
        speaker = segment.get("speaker_label", "Unknown")
        content = segment.get("content", "")
        cleaned_text.append(f"{speaker}: {content}")
    
    return "\n".join(cleaned_text)
