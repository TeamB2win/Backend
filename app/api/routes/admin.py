from fastapi import APIRouter, Body, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.events import get_db
from app.db.queries.admin import create_wanted_data
from app.db.repositories.wanted import Wanted, WantedDetail, WantedDataSource
from app.models.schemas.admin import CreateWantedDataRequest, CreateWantedDataResponse
from app.secure.hash import generate_data_hash

router = APIRouter(prefix = "/admin", tags = ["admin"])

# 데이터 추가
@router.post(
    path = "", 
    status_code=status.HTTP_201_CREATED,
    response_model=CreateWantedDataResponse
)
async def create_data(
    request : CreateWantedDataRequest = Body(..., embed = True),
    db_session : AsyncSession = Depends(get_db),
) -> CreateWantedDataResponse:
    
    wanted_data : Wanted = Wanted.create(request=request)
    wanted_data : Wanted = await create_wanted_data(db=db_session, data_table=wanted_data)

    wanted_detail_data : WantedDetail = WantedDetail.create(request=request, id=wanted_data.id)
    wanted_detail_data : WantedDetail = await create_wanted_data(db=db_session, data_table=wanted_detail_data)

    wanted_datasource_data : WantedDataSource = WantedDataSource.create(request=request, id=wanted_data.id)
    wanted_datasource_data : WantedDataSource = await create_wanted_data(db=db_session, data_table=wanted_datasource_data)

    data_hash : str = await generate_data_hash( db_session )

    return CreateWantedDataResponse(
        data_hash = data_hash,
        status = 'OK',
    )

'''
# 데이터 수정
@router.patch("/app/{criminal_id}", status_code=200)
def update_data(
'''

# 데이터 삭제
# @router.delete("/app/{criminal_id}", status_code=204)
# def delete_data(
#     criminal_id: int,
#     db_session: AsyncSession = Depends(get_db),
# ):
#     criminal: CriminalData | None = search_criminal_data(session=session, criminal_id=criminal_id)
#     if not criminal:
#         raise HTTPException(status_code=404, detail="ToDo Not Found")

#     delete_criminal_data(session=session, criminal_id=criminal_id)