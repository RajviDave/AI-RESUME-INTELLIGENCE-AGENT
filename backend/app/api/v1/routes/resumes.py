from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.api.deps import CurrentUserId, DbSession
from app.core.config import settings
from app.schemas.resume import ResumeUploadResponse
from app.services.resume_service import ResumeService

router = APIRouter()


@router.post(
    "/upload",
    response_model=ResumeUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    db: DbSession,
    current_user_id: CurrentUserId,
    file: UploadFile = File(...),
) -> ResumeUploadResponse:
    if file.content_type not in settings.allowed_upload_mime_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only PDF and DOCX resume uploads are supported.",
        )
    if Path(file.filename or "").suffix.lower() not in settings.allowed_upload_extensions:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Resume filename must end in .pdf or .docx.",
        )

    service = ResumeService(db)
    return await service.create_resume_upload(current_user_id=current_user_id, file=file)
