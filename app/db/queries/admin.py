from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.base_class import Base

from app.models.schemas.admin import UpdateWantedDataRequest, UpdateWantedVideoDataRequest
from app.db.repositories.wanted import Wanted, WantedDataSource, WantedDetail

# 범죄자 데이터 추가
async def create_wanted_data(db : AsyncSession, data_table: Base) -> Base:
    db.add(instance=data_table) # session object에 저장
    await db.flush()# 데이터베이스에 저장
    await db.refresh(instance=data_table) # 데이터베이스에서 다시 읽기
    # await db.commit()
    return data_table

async def delete_wanted_data(db : AsyncSession, id: int) -> None:
    print("Query")
    wanted_datasource_query = delete(WantedDataSource).filter(WantedDataSource.id == id) \
        .returning(WantedDataSource.image, WantedDataSource.driving_video)
    result = await db.execute(wanted_datasource_query)
    wanted_detail_query = delete(WantedDetail).filter(WantedDetail.id == id)
    await db.execute(wanted_detail_query)
    wanted_query = delete(Wanted).filter(Wanted.id == id)
    await db.execute(wanted_query)    
    return result.unique().scalars().all()

# 범죄자 데이터 수정
# async def update_wanted_data(db : AsyncSession, criminal_data: UpdateWantedVideoDataRequest) -> CreateWantedDataRequest:
#     db.add(instance=criminal_data)
#     db.commit()
#     db.refresh(instance=criminal_data)
#     return criminal_data

# 범죄자 데이터 삭제
# 

