from fastapi import FastAPI

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.app import AppSettings
from app.db.repositories.base import Base

engine = None
async_session = None

async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
    global async_session, Base, engine
    #logger.info("Connecting to PostgreSQL")

    engine = create_async_engine(settings.sync_database_url(),
                            pool_pre_ping=True,
                            echo = True,
                            )
    async_session = async_sessionmaker(autocommit=True, autoflush=False, expire_on_commit=False, bind=engine)
    Base.metadata.create_all(bind = engine)

    #logger.info("Connection established")

    return None


async def close_db_connection(app: FastAPI) -> None:
    global engine
    #logger.info("Closing connection to database")

    engine.dispose()

    #logger.info("Connection closed")

    return None

async def get_db() -> AsyncSession:
    global async_session
    async with async_session() as session:
        yield session