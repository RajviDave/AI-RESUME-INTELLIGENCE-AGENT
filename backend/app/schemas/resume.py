from uuid import UUID

from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    resume_id: UUID
    status: str
    filename: str
    content_type: str
    file_size_bytes: int
