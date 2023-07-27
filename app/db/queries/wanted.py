from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from app.db.repositories.wanted import Wanted, WantedDataSource, WantedDetail
from app.models.schemas.wanted import VideoPathRequest
async def get_full_wanted_data(db: AsyncSession) -> List[Wanted]:
    query = select(Wanted) \
            .options(joinedload(Wanted.detail, innerjoin=True)) \
            .options(joinedload(Wanted.datasource, innerjoin=True))
    
    result = await db.execute(query)
    return result.unique().scalars().all()

async def get_wanted_data(db: AsyncSession, id : int) -> List[Wanted]:
    query = select(Wanted) \
            .options(joinedload(Wanted.detail, innerjoin=True)) \
            .options(joinedload(Wanted.datasource, innerjoin=True)) \
            .filter(Wanted.id == id)
    result = await db.execute(query)
    return result.unique().scalars().first()

async def video_id_exist(db: AsyncSession, id : int) -> bool :
    query = select(WantedDataSource) \
            .filter(WantedDataSource.id == id)
    result = await db.execute(query)
    return result.unique().scalars().first() is not None

async def video_path_exist(db: AsyncSession, id : int) -> bool :
    query = select(WantedDataSource.video) \
            .filter(WantedDataSource.id == id)
    result = await db.execute(query)
    return result.unique().scalars().first() is not None

async def inject_video_path(db: AsyncSession, video_request : VideoPathRequest ) -> None :
    query = update(WantedDataSource) \
            .filter(WantedDataSource.id == video_request.id) \
            .values({
                **video_request,
                "generated" : WantedDataSource.generate + 1
            })
    await db.execute(query)
    await db.commit()
    
    return None