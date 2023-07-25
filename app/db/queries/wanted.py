from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.db.repositories.wanted import Wanted, WantedDataSource, WantedDetail

async def get_full_wanted_data(db: AsyncSession) -> List[Wanted]:
    query = select(Wanted, WantedDetail, WantedDataSource)
    query = query.options(joinedload(WantedDetail, Wanted.id == WantedDetail.id))
    query = query.options(joinedload(WantedDataSource, Wanted.id == WantedDataSource.id))

    result = await db.execute(query)
    return result.scalars().all()

async def get_wanted_data(db: AsyncSession, id : int) -> List[Wanted]:
    query = select(Wanted, WantedDetail, WantedDataSource)
    query = query.options(joinedload(WantedDetail, Wanted.id == WantedDetail.id))
    query = query.options(joinedload(WantedDataSource, Wanted.id == WantedDataSource.id))
    query = query.filter(Wanted.id == id)
    result = await db.execute(query)
    return [ result.scalars().first() ]