from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.dependencies import get_auth_service
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.core.security import create_access_token
from src.services.auth import AuthService
from src.schemas.user import UserCreate, UserRead
from src.schemas.token import Token


router = APIRouter(
    prefix='/api/auth',
    tags=['auth']
)


@router.post('/register', response_model=UserRead)
async def register(
    user_data: UserCreate,
    service: AuthService = Depends(get_auth_service)
):
    try:
        user = await service.register(user_data.email, user_data.password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )
    return UserRead.model_validate(user)


@router.post('/token', response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        service: AuthService = Depends(get_auth_service)
) -> Token:
    user = await service.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        {'sub': str(user.id), 'email': user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')
