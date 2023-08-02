from typing import Annotated
from datetime import datetime

from pydantic import Field, HttpUrl, validator
from typing import Optional
from fastapi import File, UploadFile

from app.models.schemas.base import BaseSchemaModel

# 범죄자 데이터 생성시 유저에게 요청사항
class CreateWantedDataRequest(BaseSchemaModel):
    # essential
    wanted_id : int
    wanted_type : bool
    sex : bool
    
    # optional
    name : Optional[str] = None
    age : Optional[int] = None
    height : Optional[int] = None
    weight : Optional[str] = None
    registered_address : Optional[str] = None
    residence : Optional[str] = None
    criminal : Optional[str] = None
    relational_link : Optional[str] = None
    characteristic : Optional[str] = None
    started_at : Optional[datetime] = datetime.now() # 긴급수배일 경우 현재 시간
    ended_at : Optional[datetime] = datetime.now()
     

class CreateWantedDataResponse(BaseSchemaModel):
    data_hash : str
    status : str = Field(default = 'OK')


# 범죄자 데이터 수정시 유저에게 요청
class UpdateWantedDataRequest(BaseSchemaModel):
    wanted_id : int
    name : Optional[str]
    sex : bool
    age : Optional[int]
    wanted_type : bool

    height : Optional[int]
    weight : Optional[str]
    registered_address : Optional[str]
    residence : Optional[str]
    criminal : Optional[str]
    relational_link : Optional[HttpUrl]
    characteristic : str
    started_at : datetime
    ended_at : datetime
    
    image: str

# 범죄자 비디오 데이터 DB에게 요청
class UpdateWantedVideoDataRequest(BaseSchemaModel):
    id : int
    video_url: Optional[bytes]

class CreateVideoDataToDLRequest(BaseSchemaModel) :
    id : int
    image_path : str
    wanted_type : bool
    prev_driving_path: Optional[str] = None
    video_path : Optional[str] = None


# 범죄자 데이터 삭제 요청 및 응답
class DeleteWantedRequest(BaseSchemaModel) :
    id : int

class DeleteWantedResponse(BaseSchemaModel) :
    id : int
    status : str = Field(default = 'OK')

    @validator('status')
    @classmethod
    def status_check(cls, v) :
        assert v in ['OK', 'INVALID'], ValueError('Invaild Status')
        return v