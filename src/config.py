from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = 'postgresql+asyncpg://postgres_user:postgres_password@postgres:5432/postgres_db'
    SYNC_DATABASE_URL: str = 'postgresql://postgres_user:postgres_password@postgres:5432/postgres_db'
    SECRET_KEY: str = 'cbb878e4b5e34ddd18a5251c4f592f6bcb078156dcfc2ad9d3094eaa1a60ee88'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    CORS_ORIGINS: str = 'http://localhost:3000'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()
