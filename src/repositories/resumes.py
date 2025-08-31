from typing import Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.resume import Resume


class ResumeRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_id(self, resume_id: int) -> Optional[Resume]:
        res = await self.db_session.scalar(select(Resume).where(Resume.id == resume_id))
        return res

    async def get_all(self) -> Sequence[Resume]:
        result = await self.db_session.execute(select(Resume))
        return result.scalars().all()

    async def get_all_by_user(self, user_id: int) -> Sequence[Resume]:
        result = await self.db_session.execute(
            select(Resume).where(Resume.user_id == user_id)
        )
        return result.scalars().all()

    async def create(self, title: str, content: str, user_id: Optional[int] = None) -> Resume:
        resume = Resume(title=title, content=content)
        if user_id:
            resume.user_id = user_id
        self.db_session.add(resume)
        await self.db_session.commit()
        await self.db_session.refresh(resume)
        return resume

    async def update(self, resume_id: int, title: str, content: str) -> Optional[Resume]:
        resume = await self.get_by_id(resume_id)
        if not resume:
            return None
        resume.title = title
        resume.content = content
        await self.db_session.commit()
        await self.db_session.refresh(resume)
        return resume

    async def partial_update(self, resume_id: int, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Resume]:
        resume = await self.get_by_id(resume_id)
        if not resume:
            return None
        if title is not None:
            resume.title = title
        if content is not None:
            resume.content = content
        await self.db_session.commit()
        await self.db_session.refresh(resume)
        return resume

    async def delete(self, resume_id: int) -> bool:
        res = await self.get_by_id(resume_id)
        if res:
            await self.db_session.delete(res)
            await self.db_session.commit()
            return True
        return False
