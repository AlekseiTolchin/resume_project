from typing import Optional
from pydantic import BaseModel, ConfigDict


class ResumeBase(BaseModel):
    title: str
    content: str


class ResumeCreate(ResumeBase):
    pass


class ResumeRead(ResumeBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class ImproveResumeRequest(BaseModel):
    content: str


class ImproveResumeResponse(BaseModel):
    content: str
