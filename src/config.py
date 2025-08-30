import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    'DATABASE_URL', 'postgresql+asyncpg://postgres_user:postgres_password@postgres:5432/postgres_db'
)
SYNC_DATABASE_URL = os.getenv(
    'SYNC_DATABASE_URL', 'postgresql://postgres_user:postgres_password@postgres:5432/postgres_db'
)
SECRET_KEY = os.getenv(
    'SECRET_KEY', 'cbb878e4b5e34ddd18a5251c4f592f6bcb078156dcfc2ad9d3094eaa1a60ee88'
)

ALGORITHM = os.getenv('ALGORITHM', 'HS256')

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 15)
