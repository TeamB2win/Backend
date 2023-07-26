from fastapi import APIRouter, Body, HTTPException, Depends

from Backend.app.db.db import get_db
from Backend.app.db.orm import CriminalData
from Backend.app.models.schemas.admin import CreateCriminalDataRequest, CriminalDataSchema

router = APIRouter(prefix = "/admin", tags = ["admin"])

from typing import List

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, delete



# 데이터 추가
@router.post("경로", status_code=201)
def create_criminal_data(
        request:CreateCriminalDataRequest,
        session: Session = Depends(get_db),
) -> CriminalDataSchema:
    criminal_data: CriminalData = CriminalData.create(request=request)
    criminal_data: create_criminal_data(session=session, criminal_data=criminal_data)
    return CriminalDataSchema.from_orm(criminal_data)


'''
@app.patch("경로", status_code=200)

'''
# 단일 조회 함수 만들어야함
'''

# 데이터 삭제
@app.delete("경로", status_code=204)
def delete_criminal_data(
        criminal_id: int,
        session: Session = Depends(get_db),
):
    criminal_data: CriminalData | None = get_criminal_data(session=session, criminal_id=criminal_id)
    if not criminal_data:
        raise HTTPException(status_code=404, detail="ToDo Not Found")

    delete_criminal_data(session=session, criminal_name=criminal_id)
