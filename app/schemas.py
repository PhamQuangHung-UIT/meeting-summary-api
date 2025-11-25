from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List
from datetime import datetime


# ============================
# SYSTEM_CONFIG
# ============================
class SystemConfigBase(BaseModel):
    config_key: str
    config_value: Optional[str] = None
    description: Optional[str] = None

class SystemConfigCreate(SystemConfigBase):
    pass

class SystemConfigUpdate(BaseModel):
    config_value: Optional[str] = None
    description: Optional[str] = None

class SystemConfig(SystemConfigBase):
    updated_at: Optional[datetime] = None

# ============================
# TIERS
# ============================
class TierBase(BaseModel):
    name: Optional[str] = None
    max_storage_mb: Optional[int] = None
    max_ai_minutes_monthly: Optional[int] = None

class TierCreate(TierBase):
    pass

class TierUpdate(TierBase):
    pass

class Tier(TierBase):
    tier_id: int

# ============================
# USERS
# ============================
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    tier_id: Optional[int] = None
    role: Optional[str] = "USER"
    is_active: Optional[bool] = False
    storage_used_mb: Optional[float] = 0.0

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    tier_id: Optional[int] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    storage_used_mb: Optional[float] = None

class User(UserBase):
    user_id: str
    created_at: Optional[datetime] = None

# ============================
# AUDIT_LOGS
# ============================
class AuditLogBase(BaseModel):
    user_id: Optional[str] = None
    action_type: Optional[str] = None
    ip_address: Optional[str] = None
    details: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLog(AuditLogBase):
    log_id: int
    created_at: Optional[datetime] = None

# ============================
# FOLDERS
# ============================
class FolderBase(BaseModel):
    user_id: Optional[str] = None
    name: Optional[str] = None
    parent_folder_id: Optional[str] = None

class FolderCreate(FolderBase):
    pass

class FolderUpdate(BaseModel):
    name: Optional[str] = None
    parent_folder_id: Optional[str] = None

class Folder(FolderBase):
    folder_id: str
    created_at: Optional[datetime] = None

# ============================
# RECORDINGS
# ============================
class RecordingBase(BaseModel):
    user_id: Optional[str] = None
    folder_id: Optional[str] = None
    title: Optional[str] = None
    file_path: Optional[str] = None
    duration_seconds: Optional[float] = None
    file_size_mb: Optional[float] = None
    status: Optional[str] = "UPLOADING"

class RecordingCreate(RecordingBase):
    pass

class RecordingUpdate(BaseModel):
    folder_id: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None
    deleted_at: Optional[datetime] = None

class Recording(RecordingBase):
    recording_id: str
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

# ============================
# TRANSCRIPTS
# ============================
class TranscriptBase(BaseModel):
    recording_id: Optional[str] = None
    language: Optional[str] = None
    transcript_segments: Optional[Any] = None

class TranscriptCreate(TranscriptBase):
    pass

class TranscriptUpdate(BaseModel):
    language: Optional[str] = None
    transcript_segments: Optional[Any] = None

class Transcript(TranscriptBase):
    transcript_id: str
    created_at: Optional[datetime] = None

# ============================
# SUMMARIES
# ============================
class SummaryBase(BaseModel):
    recording_id: Optional[str] = None
    type: Optional[str] = None
    content_structure: Optional[Any] = None

class SummaryCreate(SummaryBase):
    pass

class SummaryUpdate(BaseModel):
    type: Optional[str] = None
    content_structure: Optional[Any] = None

class Summary(SummaryBase):
    summary_id: str
    created_at: Optional[datetime] = None
