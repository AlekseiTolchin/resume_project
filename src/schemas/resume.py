from pydantic import BaseModel, ConfigDict


class ResumeBase(BaseModel):
    title: str
    content: str


class ResumeCreate(ResumeBase):
    pass


class ResumeRead(ResumeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
