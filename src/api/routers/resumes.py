from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from src.core.auth_dependencies import get_current_user
from src.core.dependencies import get_resume_service
from src.models.user import User
from src.services.resumes import ResumeService
from src.schemas.resume import ResumeCreate, ResumeRead, ResumeUpdate, ResumeBase, ImproveResumeResponse, ImproveResumeRequest


router = APIRouter(
    prefix='/api/resumes',
    tags=['resumes']
)


@router.post('/', response_model=ResumeRead)
async def create_resume(
        resume: ResumeCreate,
        service: ResumeService = Depends(get_resume_service),
        current_user: User = Depends(get_current_user)
):
    created_resume = await service.create_resume(resume, current_user.id)
    return ResumeRead.model_validate(created_resume)


@router.get('/', response_model=List[ResumeRead])
async def get_resumes(
        service: ResumeService = Depends(get_resume_service),
        current_user: User = Depends(get_current_user)
):
    resumes = await service.get_resumes_for_user(current_user.id)
    return [ResumeRead.model_validate(r) for r in resumes]


@router.get('/{resume_id}', response_model=ResumeRead)
async def get_resume(
        resume_id: int,
        service: ResumeService = Depends(get_resume_service),
        current_user: User = Depends(get_current_user)
):
    resume = await service.get_resume(resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resume not found'
        )
    return ResumeRead.model_validate(resume)


@router.put('/{resume_id}', response_model=ResumeRead)
async def update_resume(
        resume_id: int,
        resume: ResumeBase,
        service: ResumeService = Depends(get_resume_service),
        current_user: User = Depends(get_current_user)
):
    updated_resume = await service.update_resume(resume_id, resume, user_id=current_user.id)
    if not updated_resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resume not found or forbidden'
        )
    return ResumeRead.model_validate(updated_resume)


@router.patch('/{resume_id}', response_model=ResumeRead)
async def partial_update_resume(
        resume_id: int,
        resume: ResumeUpdate,
        service: ResumeService = Depends(get_resume_service),
        current_user: User = Depends(get_current_user)
):
    updated_resume = await service.partial_update_resume(resume_id, resume, user_id=current_user.id)
    if not updated_resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resume not found or forbidden'
        )
    return ResumeRead.model_validate(updated_resume)


@router.delete('/{resume_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: int,
    service: ResumeService = Depends(get_resume_service),
    current_user: User = Depends(get_current_user),
):
    deleted = await service.delete_resume(resume_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resume not found or forbidden'
        )


@router.post('/{resume_id}/improve', response_model=ImproveResumeResponse)
async def improve_resume_endpoint(
    resume_id: int,
    req: ImproveResumeRequest,
    service: ResumeService = Depends(get_resume_service),
    current_user: User = Depends(get_current_user)
):
    resume = await service.get_resume(resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    improved = await service.improve_resume(resume)
    return ImproveResumeResponse(content=improved)
