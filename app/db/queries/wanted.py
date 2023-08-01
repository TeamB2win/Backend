from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from app.db.repositories.wanted import Wanted, WantedDataSource, WantedDetail
from app.models.schemas.wanted import VideoPathRequest


# 범죄자 데이터 조회
async def get_full_wanted_data(db: AsyncSession) -> List[Wanted]:
    query = select(Wanted) \
            .options(joinedload(Wanted.detail, innerjoin=True)) \
            .options(joinedload(Wanted.datasource, innerjoin=True))
    
    result = await db.execute(query)
    return result.unique().scalars().all()

# 범죄자 1개 데이터 조회
async def get_wanted_data(db: AsyncSession, id : int) -> List[Wanted]:
    query = select(Wanted) \
            .options(joinedload(Wanted.detail, innerjoin=True)) \
            .options(joinedload(Wanted.datasource, innerjoin=True)) \
            .filter(Wanted.id == id)
    result = await db.execute(query)
    return result.unique().scalars().first()

#비디오 조회
async def video_id_exist(db: AsyncSession, id : int) -> bool :
    query = select(WantedDataSource) \
            .filter(WantedDataSource.id == id)
    result = await db.execute(query)
    return result.unique().scalars().first() is not None

#비디오 path 조회
async def video_path_exist(db: AsyncSession, id : int) -> bool :
    query = select(WantedDataSource.video) \
            .filter(WantedDataSource.id == id)
    result = await db.execute(query)
    return result.unique().scalars().first() is not None

#비디오 path 삽입
async def inject_video_path(db: AsyncSession, video_request : VideoPathRequest ) -> None :
    query = update(WantedDataSource) \
            .filter(WantedDataSource.id == video_request.id) \
            .values({
                "video" : video_request.video,
                "generated" : WantedDataSource.generated + 1,
                "driving_video" : video_request.driving_video,
                "error_msg" : video_request.err_msg
            })
    await db.execute(query)
    await db.commit()

    return None