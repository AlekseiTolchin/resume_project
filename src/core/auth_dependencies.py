from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import InvalidTokenError

from src.config import SECRET_KEY, ALGORITHM
from src.core.dependencies import get_auth_service
from src.services.auth import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token')


async def get_current_user(token: str = Depends(oauth2_scheme), service: AuthService = Depends(get_auth_service)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = payload.get('sub')
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except InvalidTokenError:
        raise credentials_exception
    user = await service.user_repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user
