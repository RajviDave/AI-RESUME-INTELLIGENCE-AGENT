from pathlib import Path
from asyncio import to_thread
from uuid import UUID, uuid4

from fastapi import UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.errors import AppError
from app.repositories.resume_repository import ResumeRepository
from app.schemas.resume import ResumeUploadResponse


class ResumeService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = ResumeRepository(db)

    async def create_resume_upload(
        self,
        *,
        current_user_id: UUID,
        file: UploadFile,
    ) -> ResumeUploadResponse:
        content = await file.read()
        file_size = len(content)

        if file_size == 0:
            raise AppError("Uploaded file is empty.", status.HTTP_400_BAD_REQUEST)

        if file_size > settings.max_upload_size_bytes:
            raise AppError(
                f"Uploaded file exceeds {settings.max_upload_size_mb} MB.",
                status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            )

        storage_path = await self._store_file(file.filename or "resume", content)

        resume = await self.repository.create_with_file(
            user_id=current_user_id,
            original_filename=file.filename or "resume",
            storage_path=str(storage_path),
            content_type=file.content_type or "application/octet-stream",
            file_size_bytes=file_size,
        )

        return ResumeUploadResponse(
            resume_id=resume.id,
            status=resume.status,
            filename=resume.original_filename,
            content_type=file.content_type or "application/octet-stream",
            file_size_bytes=file_size,
        )

    async def _store_file(self, filename: str, content: bytes) -> Path:
        settings.upload_dir.mkdir(parents=True, exist_ok=True)
        suffix = Path(filename).suffix.lower()
        safe_name = f"{uuid4()}{suffix}"
        destination = settings.upload_dir / safe_name
        await to_thread(destination.write_bytes, content)
        return destination
