import asyncio
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from databases.database import Base
from api.dependencies.database import get_async_db
from main import app
from models.user import User
from models.task import Task
from models.task_collaborator import TaskCollaborator
from utilities.security.password_hasher import get_password_hash

TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=True)

TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def override_get_session() -> AsyncSession:
    async with TestingSessionLocal() as session:
        print(f"⚠️ TEST DB USED: {session.bind.url}")
        yield session


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Создаёт тестовую БД перед каждым тестом и переопределяет зависимости"""
    print("⚠️ Setting up TEST database...")

    app.dependency_overrides[get_async_db] = override_get_session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def async_session() -> AsyncSession:
    """Фикстура для передачи сессии в тесты"""
    async with TestingSessionLocal() as session:
        yield session
        await session.close()


@pytest_asyncio.fixture()
async def http_client():
    """Фикстура для тестового клиента"""
    async with AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as client:
        yield client


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Использует единый event loop для всех тестов"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def user_fixture(async_session: AsyncSession) -> User:
    user = User(
        username="TestuSER",
        password=get_password_hash("secret")
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def another_user_fixture(async_session: AsyncSession) -> User:
    user = User(
        username="AnotherUser",
        password=get_password_hash("qwerty")
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def task_fixture(
    async_session: AsyncSession, user_fixture: User
) -> Task:
    task = Task(
        title="Test Task",
        description="Test description",
        owner_id=user_fixture.id
    )
    async_session.add(task)
    await async_session.commit()
    await async_session.refresh(task)
    return task


@pytest_asyncio.fixture
async def another_task_fixture(
    async_session: AsyncSession, another_user_fixture: User
) -> Task:
    task = Task(
        title="Another Test Task",
        description="Another test description",
        owner_id=another_user_fixture.id,
    )
    async_session.add(task)
    await async_session.commit()
    await async_session.refresh(task)
    return task


@pytest_asyncio.fixture
async def collaborator_fixture(
    async_session: AsyncSession,
    task_fixture: Task,
    another_user_fixture: User,
) -> TaskCollaborator:
    collaborator = TaskCollaborator(
        task_id=task_fixture.id,
        user_id=another_user_fixture.id,
        can_read=True,
        can_update=True
    )
    async_session.add(collaborator)
    await async_session.commit()
    await async_session.refresh(collaborator)
    return collaborator
