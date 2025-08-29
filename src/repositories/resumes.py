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

    async def get_all_by_user(self, user_id: int) -> Sequence[Resume]:
        res = await self.db_session.scalars(select(Resume).where(Resume.user_id == user_id))
        return res.all()

    async def create(self, title: str, content: str, user_id: Optional[int] = None) -> Resume:
        res = Resume(title=title, content=content)
        if user_id is not None:
            res.user_id = user_id
        self.db_session.add(res)
        await self.db_session.commit()
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

    async def partial_update(self, resume_id: int, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Resume]:
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
        res = await self.get_by_id(resume_id)
        if res:
            await self.db_session.delete(res)
            await self.db_session.commit()
            return True
        return False
