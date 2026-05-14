from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.core.security import create_access_token, get_password_hash, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.users = UserRepository(db)

    async def register(self, *, email: str, password: str) -> AuthResponse:
        existing_user = await self.users.get_by_email(email)
        if existing_user is not None:
            raise AppError("A user with this email already exists.", status.HTTP_409_CONFLICT)

        user = await self.users.create(email=email, hashed_password=get_password_hash(password))
        token = create_access_token(subject=str(user.id))
        return AuthResponse(user_id=user.id, email=user.email, access_token=token)

    async def login(self, *, email: str, password: str) -> AuthResponse:
        user = await self.users.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            raise AppError("Invalid email or password.", status.HTTP_401_UNAUTHORIZED)

        token = create_access_token(subject=str(user.id))
        return AuthResponse(user_id=user.id, email=user.email, access_token=token)
