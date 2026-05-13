from fastapi import APIRouter, status

from app.api.deps import DbSession
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(db: DbSession, payload: RegisterRequest) -> AuthResponse:
    return await AuthService(db).register(email=payload.email, password=payload.password)


@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def login(db: DbSession, payload: LoginRequest) -> AuthResponse:
    return await AuthService(db).login(email=payload.email, password=payload.password)
