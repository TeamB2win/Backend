from typing import Optional, List, Any

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.base_class import Base

from app.models.schemas.admin import UpdateWantedDataRequest, UpdateWantedMediaRequest
from app.db.repositories.wanted import Wanted, WantedDataSource, WantedDetail

table_dict = {
    'wanted' : Wanted,
    'wanted_datasource' : WantedDataSource,
    'wanted_detail' : WantedDetail
}

# 범죄자 데이터 추가
async def create_wanted_data(db : AsyncSession, data_table: Base) -> Base:
    db.add(instance=data_table) # session object에 저장
    await db.flush()# 데이터베이스에 저장
    await db.refresh(instance=data_table) # 데이터베이스에서 다시 읽기
    # await db.commit()
    return data_table

async def delete_wanted_data(db : AsyncSession, id: int) -> List[Any]:
    print("Query")
    wanted_datasource_query = delete(WantedDataSource).filter(WantedDataSource.id == id) \
        .returning(WantedDataSource.image, WantedDataSource.driving_video)
    result = await db.execute(wanted_datasource_query)
    wanted_detail_query = delete(WantedDetail).filter(WantedDetail.id == id)
    await db.execute(wanted_detail_query)
    wanted_query = delete(Wanted).filter(Wanted.id == id)
    await db.execute(wanted_query)    
    return result.unique().scalars().all()

async def update_wanted_data(db: AsyncSession, table_type: str, request : UpdateWantedDataRequest ) -> None :
    table = table_dict[table_type]
    query = update(table) \
        .filter(table.id == request.id) \
        .values({
            **table.convert_dict(request)
        })
    await db.execute(query)
    await db.flush()
    return None

async def update_wanted_datasource(db: AsyncSession, id : int, image_path : str ) -> List[Any] :
    query = update(WantedDataSource) \
        .filter(WantedDataSource.id == id) \
        .values({
            'image' : image_path,
        }) \
        .returning(WantedDataSource)
    result = await db.execute(query)
    await db.flush()
    return result.first()[0]

