from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Meeting(BaseModel):
    title: Optional[str] = None
    attendees: Optional[List[str]] = []
    notes: str


class Summary(BaseModel):
    summary: str


app = FastAPI(title="Meeting Summary API")


@app.get("/", summary="Health check")
def read_root():
    return {"status": "ok", "message": "Meeting Summary API"}


@app.post("/summarize", response_model=Summary, summary="Summarize meeting notes")
def summarize(meeting: Meeting):
    """A tiny, deterministic summarizer used as an example. Replace with a real ML model or external service.

    Current strategy (very simple):
    - If notes are empty -> empty summary
    - Return the first sentence if it looks long enough
    - Else return up to the first 200 characters
    """
    text = (meeting.notes or "").strip()
    if not text:
        return {"summary": ""}

    # Get the first sentence-like chunk
    first_sentence = text.split(".")[0].strip()
    if len(first_sentence) >= 20:
        summary = first_sentence + "."
    else:
        summary = text[:200] + ("..." if len(text) > 200 else "")

    return {"summary": summary}
