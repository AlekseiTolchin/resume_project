from src.repositories.users import UserRepository
from src.core.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, email: str, password: str):
        if await self.user_repo.get_by_email(email):
            raise ValueError("User already exists")
        return await self.user_repo.create(email, hash_password(password))

    async def authenticate(self, email: str, password: str):
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def create_token(self, user):
        return create_access_token({'sub': str(user.id), 'email': user.email})
