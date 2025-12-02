from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List
from datetime import datetime
from enum import Enum


# ============================
# ENUMS
# ============================
class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class RecordingStatus(str, Enum):
    UPLOADING = "UPLOADING"
    PROCESSED = "PROCESSED"
    ERROR = "ERROR"

class SummaryType(str, Enum):
    AI_GENERATED = "AI_GENERATED"
    USER_EDITED = "USER_EDITED"

class ActionType(str, Enum):
    UPLOAD = "UPLOAD"
    SUMMARIZE = "SUMMARIZE"
    DELETE = "DELETE"
    UPDATE = "UPDATE"
    DOWNLOAD = "DOWNLOAD"
    SHARE = "SHARE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"


# ============================
# SYSTEM_CONFIG
# ============================
class SystemConfigBase(BaseModel):
    config_key: str
    config_value: str
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
    name: str
    max_storage_mb: int
    max_ai_minutes_monthly: int

class TierCreate(TierBase):
    pass

class TierUpdate(BaseModel):
    name: Optional[str] = None
    max_storage_mb: Optional[int] = None
    max_ai_minutes_monthly: Optional[int] = None

class Tier(TierBase):
    tier_id: int
    created_at: Optional[datetime] = None


# ============================
# USERS
# ============================
class UserBase(BaseModel):
    email: str
    full_name: str
    tier_id: int
    role: Optional[UserRole] = UserRole.USER
    is_active: Optional[bool] = True
    storage_used_mb: Optional[float] = 0.0

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    tier_id: Optional[int] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    storage_used_mb: Optional[float] = None

class User(UserBase):
    user_id: str
    created_at: Optional[datetime] = None


# ============================
# AUDIT_LOGS
# ============================
class AuditLogBase(BaseModel):
    user_id: str
    action_type: ActionType
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
    user_id: str
    name: str
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
    user_id: str
    folder_id: Optional[str] = None
    title: str
    file_path: str
    duration_seconds: Optional[float] = None
    file_size_mb: float
    status: Optional[RecordingStatus] = RecordingStatus.UPLOADING

class RecordingCreate(RecordingBase):
    pass

class RecordingUpdate(BaseModel):
    folder_id: Optional[str] = None
    title: Optional[str] = None
    status: Optional[RecordingStatus] = None
    duration_seconds: Optional[float] = None
    deleted_at: Optional[datetime] = None

class Recording(RecordingBase):
    recording_id: str
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


# ============================
# TRANSCRIPTS
# ============================
class TranscriptBase(BaseModel):
    recording_id: str
    language: str
    confidence_score: Optional[float] = None

class TranscriptCreate(TranscriptBase):
    pass

class TranscriptUpdate(BaseModel):
    language: Optional[str] = None
    confidence_score: Optional[float] = None

class Transcript(TranscriptBase):
    transcript_id: str
    created_at: Optional[datetime] = None


# ============================
# TRANSCRIPT SEGMENTS
# ============================
class TranscriptSegmentBase(BaseModel):
    transcript_id: str
    start_time: float
    end_time: float
    content: str
    speaker_label: Optional[str] = None

class TranscriptSegmentCreate(TranscriptSegmentBase):
    pass

class TranscriptSegmentUpdate(BaseModel):
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    content: Optional[str] = None
    speaker_label: Optional[str] = None

class TranscriptSegment(TranscriptSegmentBase):
    segment_id: int


# ============================
# RECORDING SPEAKERS
# ============================
class RecordingSpeakerBase(BaseModel):
    recording_id: str
    speaker_label: str
    display_name: Optional[str] = None

class RecordingSpeakerCreate(RecordingSpeakerBase):
    pass

class RecordingSpeakerUpdate(BaseModel):
    display_name: Optional[str] = None

class RecordingSpeaker(RecordingSpeakerBase):
    id: int


# ============================
# SUMMARIES
# ============================
class SummaryBase(BaseModel):
    recording_id: str
    type: SummaryType
    content_structure: Dict[str, Any]

class SummaryCreate(SummaryBase):
    pass

class SummaryUpdate(BaseModel):
    type: Optional[SummaryType] = None
    content_structure: Optional[Dict[str, Any]] = None

class Summary(SummaryBase):
    summary_id: str
    created_at: Optional[datetime] = None
