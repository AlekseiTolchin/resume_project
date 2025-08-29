from typing import Sequence, Optional

from src.repositories.resumes import ResumeRepository
from src.schemas.resume import ResumeCreate, ResumeUpdate
from src.models.resume import Resume


class ResumeService:
    def __init__(self, resume_repo: ResumeRepository):
        self.resume_repo = resume_repo

    async def get_resume(self, resume_id: int) -> Optional[Resume]:
        resume = await self.resume_repo.get_by_id(resume_id)
        return resume

    async def get_resumes_for_user(self, user_id: int) -> Sequence[Resume]:
        return await self.resume_repo.get_all_by_user(user_id)

    async def create_resume(self, data: ResumeCreate, user_id: int) -> Resume:
        return await self.resume_repo.create(title=data.title, content=data.content, user_id=user_id)

    async def update_resume(self,resume_id: int, data: ResumeUpdate, user_id: int) -> Optional[Resume]:
        resume = await self.resume_repo.get_by_id(resume_id)
        if not resume or resume.user_id != user_id:
            return None
        return await self.resume_repo.partial_update(resume_id, title=data.title, content=data.content)

    async def delete_resume(self, resume_id: int, user_id: int) -> bool:
        resume = await self.resume_repo.get_by_id(resume_id)
        if not resume or resume.user_id != user_id:
            return False
        return await self.resume_repo.delete(resume_id)

    async def improve_resume(self, resume: Resume) -> str:
        return resume.content + "[Improved]"
