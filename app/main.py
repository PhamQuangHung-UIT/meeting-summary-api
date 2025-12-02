from fastapi import FastAPI

# Keep the application factory / app object here and include routers from submodules.
from app.auth import router as auth_router
from app.routers import (
    system_config,
    audit_logs,
    users,
    tiers,
    folders,
    recordings,
    recording_speakers,
    transcripts,
    transcript_segments,
    summaries
)


app = FastAPI(title="Meeting Summary API")

# include auth endpoints
app.include_router(auth_router)
app.include_router(system_config.router)
app.include_router(audit_logs.router)
app.include_router(users.router)
app.include_router(tiers.router)
app.include_router(folders.router)
app.include_router(recordings.router)
app.include_router(recording_speakers.router)
app.include_router(transcripts.router)
app.include_router(transcript_segments.router)
app.include_router(summaries.router)


@app.get("/", summary="Health check")
def read_root():
    return {"status": "ok", "message": "Meeting Summary API"}
