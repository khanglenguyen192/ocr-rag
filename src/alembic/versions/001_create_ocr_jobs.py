"""create ocr_jobs table

Revision ID: 001
Revises:
Create Date: 2026-03-16
"""
from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ocr_jobs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("job_type", sa.String(20), nullable=False, index=True),
        sa.Column("source_ref", sa.Text(), nullable=False),
        sa.Column("original_filename", sa.String(500), nullable=True),
        sa.Column("result_md", sa.Text(), nullable=True),
        sa.Column("page_count", sa.Integer(), server_default="0"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_ocr_jobs_job_type", "ocr_jobs", ["job_type"])


def downgrade() -> None:
    op.drop_index("ix_ocr_jobs_job_type", table_name="ocr_jobs")
    op.drop_table("ocr_jobs")

