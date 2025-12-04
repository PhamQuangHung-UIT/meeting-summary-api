from fastapi import APIRouter, HTTPException, status
from typing import List

from app import schemas
from app.services.ai_usage_log_service import AiUsageLogService

router = APIRouter(prefix="/ai_usage_logs", tags=["AI Usage Logs"])

@router.get("/", response_model=List[schemas.AiUsageLog])
def get_all_ai_usage_logs():
    return AiUsageLogService.get_all_ai_usage_logs()

@router.get("/{usage_id}", response_model=schemas.AiUsageLog)
def get_ai_usage_log(usage_id: int):
    log = AiUsageLogService.get_ai_usage_log_by_id(usage_id)
    if not log:
        raise HTTPException(status_code=404, detail="AI Usage Log not found")
    return log

@router.post("/", response_model=schemas.AiUsageLog, status_code=status.HTTP_201_CREATED)
def create_ai_usage_log(log: schemas.AiUsageLogCreate):
    return AiUsageLogService.create_ai_usage_log(log)

@router.delete("/{usage_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ai_usage_log(usage_id: int):
    AiUsageLogService.delete_ai_usage_log(usage_id)
    return None
