from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.repositories.wanted import Wanted, WantedDataSource, WantedDetail

def get_full_wanted_data(db: AsyncSession) -> List[Wanted]:
    query = db.execute(select(Wanted))
    query = query.join(WantedDetail, Wanted.id == WantedDetail.id)
    query = query.join(WantedDataSource, Wanted.id == WantedDataSource.id)
    return query.all()

def get_wanted_data(db: AsyncSession, id : int) -> List[Wanted]:
    query = db.execute(select(Wanted))
    query = query.join(WantedDetail, Wanted.id == WantedDetail.id)
    query = query.join(WantedDataSource, Wanted.id == WantedDataSource.id)
    return [ query.filter(Wanted.id == id).first() ]