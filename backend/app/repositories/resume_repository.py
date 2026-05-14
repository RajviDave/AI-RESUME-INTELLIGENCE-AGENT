from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume, ResumeFile


class ResumeRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_with_file(
        self,
        *,
        user_id: UUID,
        original_filename: str,
        storage_path: str,
        content_type: str,
        file_size_bytes: int,
    ) -> Resume:
        resume = Resume(user_id=user_id, original_filename=original_filename)
        self.db.add(resume)
        await self.db.flush()

        resume_file = ResumeFile(
            resume_id=resume.id,
            storage_path=storage_path,
            content_type=content_type,
            file_size_bytes=file_size_bytes,
        )
        self.db.add(resume_file)
        await self.db.commit()
        await self.db.refresh(resume)
        return resume
