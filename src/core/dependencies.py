from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import async_session
from src.repositories.resumes import ResumeRepository
from src.repositories.users import UserRepository
from src.services.auth import AuthService
from src.services.resumes import ResumeService


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


def get_resume_repository(db_session: AsyncSession = Depends(get_db_session)) -> ResumeRepository:
    return ResumeRepository(db_session=db_session)


def get_resume_service(db_session: AsyncSession = Depends(get_db_session)) -> ResumeService:
    return ResumeService(resume_repo=ResumeRepository(db_session=db_session))


def get_user_repository(db_session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


def get_auth_service(db_session: AsyncSession = Depends(get_db_session)) -> AuthService:
    return AuthService(user_repo=UserRepository(db_session=db_session))
