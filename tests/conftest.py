import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.core.auth_dependencies import get_current_user
from src.core.database import Base
from src.core.dependencies import get_db_session
from src.models.user import User
from src.models.resume import Resume


TEST_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'


@pytest_asyncio.fixture
async def test_engine():
    """Асинхронный SQLAlchemy engine для тестовой SQLite-базы (in-memory)."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def async_sessionmaker(test_engine):
    """Возвратить асинхронный sessionmaker для тестовой БД."""
    return sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def override_get_async_session(async_sessionmaker):
    """
    Переопределить зависимость get_db_session и возвратить сессии для тестовой БД.
    """
    async def _override():
        async with async_sessionmaker() as session:
            yield session
    app.dependency_overrides[get_db_session] = _override
    yield
    app.dependency_overrides.pop(get_db_session, None)


def dummy_user():
    """
    Возвратить фиктивного пользователя для тестов.
    """
    user = User(
        id=123,
        email="test@example.com",
        hashed_password="notarealhash"
    )
    user.resumes = []
    return user


async def override_get_current_user():
    """
    Возвратить фиктивного пользователя для подмены зависимости get_current_user.
    """
    return dummy_user()


@pytest_asyncio.fixture
async def client():
    """
    Вернуть асинхронного тестового клиента для FastAPI-приложения.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as c:
        yield c


@pytest.fixture(autouse=True)
def override_current_user():
    """
    Переопределить зависимость get_current_user для тестов (выдать фиктивного пользователя).
    """
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest_asyncio.fixture
async def create_resume(async_sessionmaker):
    """
    Создать и сохранить тестовое резюме для пользователя с user_id=123 в тестовой базе данных.
    """
    async with async_sessionmaker() as session:
        resume = Resume(
            title='Тестовое резюме',
            content='Текст резюме',
            user_id=123,
        )
        session.add(resume)
        await session.commit()
        await session.refresh(resume)
        yield resume


@pytest_asyncio.fixture(autouse=True)
async def clear_resumes_table(async_sessionmaker):
    """Очистить таблицу resumes перед каждым тестом."""
    async with async_sessionmaker() as session:
        await session.execute(delete(Resume))
        await session.commit()


@pytest_asyncio.fixture(autouse=True)
async def clear_users_table(async_sessionmaker):
    """Очистить таблицу users перед каждым тестом"""
    async with async_sessionmaker() as session:
        await session.execute(delete(User))
        await session.commit()
