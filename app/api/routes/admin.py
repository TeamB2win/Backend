from fastapi import FastAPI, Body, HTTPException, Depends

from db.db import get_db
from db.orm import CriminalData
from models.domain.admin import create_criminal_data, search_criminal_data, search_criminals_data, delete_criminal_data
from models.schemas.admin import CreateCriminalDataRequest, CriminalDataSchema, ListCriminalDataResponse
#router = APIRouter(prefix = "/admin", tags = ["admin"])

router = FastAPI()

from typing import List

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, delete


# 전체 데이터 조회
@router.get("/app", status_code=200)
def search_criminals(
    order: str | None = None,
    session: Session = Depends(get_db),
) -> ListCriminalDataResponse:
    criminal_data_list: List[CriminalData] = search_criminals_data(session=session)
    return ListCriminalDataResponse(
        #criminal_data_list=[CriminalDataSchema.from_orm(criminal_data) for criminal_data in criminal_data_list]
        CriminalData = criminal_data_list
    )          


# 데이터 추가
@router.post("/app", status_code=201)
def create_data(
        request:CreateCriminalDataRequest,
        session:Session = Depends(get_db),
) -> CriminalDataSchema:
    criminal_data: CriminalData = CriminalData.create(request=request)
    criminal_data: CriminalData = create_criminal_data(session=session, criminal_data=criminal_data)
    return CriminalDataSchema.from_orm(criminal_data)

'''
# 데이터 수정
@router.patch("/app/{criminal_id}", status_code=200)
def update_data(
'''

# 데이터 삭제
@router.delete("/app/{criminal_id}", status_code=204)
def delete_data(
        criminal_id: int,
        session: Session = Depends(get_db),
):
    criminal: CriminalData | None = search_criminal_data(session=session, criminal_id=criminal_id)
    if not criminal:
        raise HTTPException(status_code=404, detail="ToDo Not Found")

    delete_criminal_data(session=session, criminal_id=criminal_id)