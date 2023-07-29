from typing import Annotated
from datetime import datetime

from pydantic import Field, HttpUrl
from typing import Optional
from fastapi import File

from app.models.schemas.base import BaseSchemaModel

# 범죄자 데이터 생성시 유저에게 요청사항
class CreateWantedDataRequest(BaseSchemaModel):
    # essential
    wanted_id : int
    wanted_type : bool
    sex : bool
    image : Annotated[bytes, File()]
    
    # optional
    name : Optional[str] = None
    age : Optional[int] = None
    height : Optional[int] = Field(default=None)
    weight : Optional[str] = Field(default=None)
    registered_address : Optional[str] = Field(default=None)
    residence : Optional[str] = Field(default=None)
    criminal : Optional[str] = Field(default=None)
    relational_link : Optional[HttpUrl] = Field(default=None)
    characteristic : str = Field(default=None)
    started_at : Optional[datetime] = Field(default=datetime.now())
    ended_at : Optional[datetime] = Field(default=datetime.now())
    

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
    
    image : Annotated[bytes, File()]

# 범죄자 비디오 데이터 DB에게 요청
class UpdateWantedVideoDataRequest(BaseSchemaModel):
    id : int
    video_url: Optional[bytes]