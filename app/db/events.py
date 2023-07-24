import asyncpg
from databases import Database

from fastapi import FastAPI
from loguru import logger
from sqlalchemy import (Column, Integer, String, Table, create_engine, MetaData)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from app.config.app import AppSettings


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to PostgreSQL")

    # app.state.pool = await asyncpg.create_pool(
    #     str(settings.database_url),
    #     min_size=settings.min_connection_count,
    #     max_size=settings.max_connection_count,
    # )
    engine = create_engine(settings.database_url,
                           echo = True,
                           connect_args = {'check_same_thread' : False})
    session = sessionmaker(autocommit=True, autoflush=False, bind=engine)
    Base = declarative_base()

    logger.info("Connection established")

    return None


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.pool.close()

    logger.info("Connection closed")

    return None