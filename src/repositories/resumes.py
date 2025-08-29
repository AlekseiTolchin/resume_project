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
        res = await self.db_session.scalars(select(Resume))
        return res.all()

    async def create(self, title: str, content: str) -> Resume:
        res = Resume(title=title, content=content)
        self.db_session.add(res)
        await self.db_session.refresh(res)
        return res

    async def update(self, resume_id: int, title: str, content: str) -> Optional[Resume]:
        res = await self.db_session.scalar(select(Resume).where(Resume.id == resume_id))
        if not res:
            return None
        res.title = title
        res.content = content
        await self.db_session.commit()
        await self.db_session.refresh(res)
        return res

    async def partial_update(self, resume_id: int, title: Optional[str] = None, content: Optional[str] = None) -> \
    Optional[Resume]:
        res = await self.db_session.scalar(select(Resume).where(Resume.id == resume_id))
        if not res:
            return None
        if title is not None:
            res.title = title
        if content is not None:
            res.content = content
        await self.db_session.commit()
        await self.db_session.refresh(res)
        return res

    async def delete(self, resume_id: int) -> bool:
        db_resume = await self.get_by_id(resume_id)
        if db_resume:
            await self.db_session.delete(db_resume)
            await self.db_session.commit()
            return True
        return False
