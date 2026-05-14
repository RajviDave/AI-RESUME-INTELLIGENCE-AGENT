from enum import StrEnum
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.mixins import TimestampMixin


class ResumeStatus(StrEnum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Resume(TimestampMixin, Base):
    __tablename__ = "resumes"

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default=ResumeStatus.UPLOADED.value, nullable=False)

    user: Mapped["User"] = relationship(back_populates="resumes")
    file: Mapped["ResumeFile"] = relationship(back_populates="resume", uselist=False)


class ResumeFile(TimestampMixin, Base):
    __tablename__ = "resume_files"

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True, default=uuid4)
    resume_id: Mapped[UUID] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
    storage_path: Mapped[str] = mapped_column(Text, nullable=False)
    content_type: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)

    resume: Mapped[Resume] = relationship(back_populates="file")
