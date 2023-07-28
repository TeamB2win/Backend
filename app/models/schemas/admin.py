from datetime import datetime

from pydantic import Field, HttpUrl
from typing import List, Optional

from app.models.schemas.base import BaseSchemaModel
from app.models.domain.wanted import WantedFullData

# 범죄자 데이터 생성시 유저에게 요청사항
class CreateWantedDataRequest(BaseSchemaModel):
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
    
    image : str
    video : Optional[str]
    generated : int
    driving_video : Optional[str] = None
    error_msg : Optional[str] = None

class CreateWantedDataResponse(BaseSchemaModel):
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
    
    image : str
    video : Optional[str]
    generated : int
    driving_video : Optional[str] = None
    error_msg : Optional[str] = None

# 범죄자 비디오 데이터 DB에게 요청
class UpdateWantedVideoDataRequest(BaseSchemaModel):
    id : int
    video_url: Optional[bytes]