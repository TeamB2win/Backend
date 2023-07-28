from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.base_class import Base

from app.models.schemas.admin import UpdateWantedDataRequest, UpdateWantedVideoDataRequest
from app.db.repositories.wanted import Wanted, WantedDataSource, WantedDetail

# 범죄자 데이터 추가
async def create_wanted_data(db : AsyncSession, data_table: Base) -> Base:
    db.add(instance=data_table) # session object에 저장
    db.commit() # 데이터베이스에 저장
    db.refresh(instance=data_table) # 데이터베이스에서 다시 읽기
    return data_table

# 범죄자 데이터 수정
# async def update_wanted_data(db : AsyncSession, criminal_data: UpdateWantedVideoDataRequest) -> CreateWantedDataRequest:
#     db.add(instance=criminal_data)
#     db.commit()
#     db.refresh(instance=criminal_data)
#     return criminal_data

# 범죄자 데이터 삭제
# async def delete_criminal_data(db : AsyncSession, criminal_id: int) -> None:
#     db.execute(delete(Wanted).where(CriminalData.id == criminal_id))
#     db.commit()

