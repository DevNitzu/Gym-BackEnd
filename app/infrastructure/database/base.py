from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# 🚀 Cambiar la URL para async
async_database_url = settings.database_url.replace("mysql+pymysql://", "mysql+aiomysql://")

# Crear engine async
engine = create_async_engine(async_database_url, echo=True)

# Async session maker
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Base
Base = declarative_base()

# Dependencia FastAPI
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
