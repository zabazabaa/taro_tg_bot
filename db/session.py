from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from db.models import Base

engine = create_async_engine(
    'sqlite+aiosqlite:///db.sqlite', 
    echo=True
)

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)