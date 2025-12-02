CREATE TYPE user_role AS ENUM ('USER', 'ADMIN');

CREATE TYPE recording_source_type AS ENUM ('RECORDED', 'IMPORTED');

CREATE TYPE recording_status AS ENUM ('UPLOADING', 'PROCESSED', 'ERROR');

CREATE TYPE transcript_type AS ENUM ('AI_ORIGINAL', 'USER_EDITED', 'REGENERATED');

CREATE TYPE summary_type AS ENUM ('AI_GENERATED', 'USER_EDITED');

CREATE TYPE marker_type AS ENUM ('NORMAL', 'HIGHLIGHT');

CREATE TYPE export_status AS ENUM ('PENDING', 'PROCESSING', 'DONE', 'FAILED');

CREATE TYPE audit_status AS ENUM ('SUCCESS', 'FAILED');

-- =============================================
-- CREATE TABLES
-- =============================================

-- 1. SYSTEM_CONFIG
CREATE TABLE system_config (
    config_key VARCHAR(255) PRIMARY KEY,
    config_value TEXT NOT NULL,
    description TEXT,
    config_group VARCHAR(100),
    is_sensitive BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. TIERS
CREATE TABLE tiers (
    tier_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    max_storage_mb INTEGER NOT NULL,
    max_ai_minutes_monthly INTEGER NOT NULL,
    max_recordings INTEGER NOT NULL,
    max_duration_per_recording_sec INTEGER NOT NULL,
    allow_diarization BOOLEAN DEFAULT FALSE,
    allow_summarization BOOLEAN DEFAULT FALSE,
    price_monthly DECIMAL(10, 2) DEFAULT 0
);

-- 3. USERS
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(255),
    tier_id INTEGER REFERENCES tiers(tier_id) ON DELETE SET NULL,
    role user_role DEFAULT 'USER',
    is_active BOOLEAN DEFAULT TRUE,
    storage_used_mb DECIMAL(10, 2) DEFAULT 0,
    email_verified BOOLEAN DEFAULT FALSE,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

-- 4. AUDIT_LOGS
CREATE TABLE audit_logs (
    log_id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    action_type VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id UUID,
    ip_address VARCHAR(50),
    status audit_status NOT NULL,
    error_code VARCHAR(50),
    details TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. FOLDERS
CREATE TABLE folders (
    folder_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    parent_folder_id UUID REFERENCES folders(folder_id) ON DELETE CASCADE,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

-- 6. RECORDINGS
CREATE TABLE recordings (
    recording_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    folder_id UUID REFERENCES folders(folder_id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    duration_seconds DECIMAL(10, 2) NOT NULL,
    file_size_mb DECIMAL(10, 2) NOT NULL,
    source_type recording_source_type NOT NULL,
    original_file_name VARCHAR(255),
    status recording_status DEFAULT 'UPLOADING',
    is_pinned BOOLEAN DEFAULT FALSE,
    is_trashed BOOLEAN DEFAULT FALSE,
    auto_title BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

-- 7. TRANSCRIPTS
CREATE TABLE transcripts (
    transcript_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID NOT NULL REFERENCES recordings(recording_id) ON DELETE CASCADE,
    version_no INTEGER NOT NULL,
    type transcript_type NOT NULL,
    language VARCHAR(10),
    confidence_score DECIMAL(5, 4),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(recording_id, version_no)
);

-- 8. TRANSCRIPT_SEGMENTS
CREATE TABLE transcript_segments (
    segment_id BIGSERIAL PRIMARY KEY,
    transcript_id UUID NOT NULL REFERENCES transcripts(transcript_id) ON DELETE CASCADE,
    sequence INTEGER NOT NULL,
    start_time DECIMAL(10, 2) NOT NULL,
    end_time DECIMAL(10, 2) NOT NULL,
    content TEXT NOT NULL,
    speaker_label VARCHAR(50),
    confidence DECIMAL(5, 4),
    is_user_edited BOOLEAN DEFAULT FALSE
);

-- 9. RECORDING_SPEAKERS
CREATE TABLE recording_speakers (
    id BIGSERIAL PRIMARY KEY,
    recording_id UUID NOT NULL REFERENCES recordings(recording_id) ON DELETE CASCADE,
    speaker_label VARCHAR(50) NOT NULL,
    display_name VARCHAR(255),
    color VARCHAR(20),
    UNIQUE(recording_id, speaker_label)
);

-- 10. SUMMARIES
CREATE TABLE summaries (
    summary_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID NOT NULL REFERENCES recordings(recording_id) ON DELETE CASCADE,
    version_no INTEGER NOT NULL,
    type summary_type NOT NULL,
    summary_style VARCHAR(50),
    content_structure JSONB,
    is_latest BOOLEAN DEFAULT TRUE,
    generated_by UUID REFERENCES users(user_id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(recording_id, version_no)
);

-- 11. AI_USAGE_LOGS
CREATE TABLE ai_usage_logs (
    usage_id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    recording_id UUID REFERENCES recordings(recording_id) ON DELETE SET NULL,
    action_type VARCHAR(50) NOT NULL,
    duration_seconds DECIMAL(10, 2) NOT NULL,
    ai_minutes_charged DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 12. MARKERS
CREATE TABLE markers (
    marker_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID NOT NULL REFERENCES recordings(recording_id) ON DELETE CASCADE,
    time_seconds DECIMAL(10, 2) NOT NULL,
    label TEXT,
    type marker_type DEFAULT 'NORMAL',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 13. EXPORT_JOBS
CREATE TABLE export_jobs (
    export_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    recording_id UUID NOT NULL REFERENCES recordings(recording_id) ON DELETE CASCADE,
    export_type VARCHAR(50) NOT NULL,
    status export_status DEFAULT 'PENDING',
    file_path TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- 14. RECORDING_TAGS
CREATE TABLE recording_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID NOT NULL REFERENCES recordings(recording_id) ON DELETE CASCADE,
    tag VARCHAR(100) NOT NULL
);