-- ============================================================
-- OCR Web Platform — Database Schema
-- Database: pgocr (PostgreSQL 14+)
-- Run: psql -U postgres -d pgocr -f scripts/create_tables.sql
-- ============================================================

-- Đảm bảo extension uuid nếu cần sau này
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── Drop nếu đã tồn tại (dev only) ───────────────────────────
-- DROP TABLE IF EXISTS ocr_jobs;

-- ── Schema: pgdbo ─────────────────────────────────────────────
CREATE SCHEMA IF NOT EXISTS pgdbo;
SET search_path TO pgdbo;

-- ── Table: ocr_jobs ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ocr_jobs (
    id               SERIAL          PRIMARY KEY,
    job_type         VARCHAR(20)     NOT NULL,
    -- 'pdf_digital' | 'pdf_scanned' | 'image' | 'youtube'

    source_ref       TEXT            NOT NULL,
    -- Tên file gốc hoặc YouTube URL

    original_filename VARCHAR(500)   NULL,
    -- Tên file người dùng upload

    result_md        TEXT            NULL,
    -- Kết quả Markdown sau khi OCR / transcript

    page_count       INTEGER         NOT NULL DEFAULT 0,
    -- Số trang đã xử lý (PDF), = 1 với ảnh / YouTube

    created_at       TIMESTAMP       NOT NULL DEFAULT NOW()
    -- Thời điểm tạo record
);

-- ── Indexes ───────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS ix_ocr_jobs_job_type   ON ocr_jobs (job_type);
CREATE INDEX IF NOT EXISTS ix_ocr_jobs_created_at ON ocr_jobs (created_at DESC);

-- ── Verify ───────────────────────────────────────────────────
SELECT
    column_name,
    data_type,
    character_maximum_length,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'ocr_jobs'
ORDER BY ordinal_position;

