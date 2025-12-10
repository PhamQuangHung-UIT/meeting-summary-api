from fastapi import APIRouter, HTTPException, status
from typing import List

from app import schemas
from app.services.recording_tag_service import RecordingTagService

router = APIRouter(prefix="/recording_tags", tags=["Recording Tags"])

# Tag management is moved to recordings router as sub-resources
# POST /recordings/:id/tags
# DELETE /recordings/:id/tags/:tag
