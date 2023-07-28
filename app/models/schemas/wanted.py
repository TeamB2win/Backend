from typing import Optional, List
from pydantic import Field, validator
from app.models.schemas.base import BaseSchemaModel
from app.models.domain.wanted import WantedFullData

class WantedDataResponse(BaseSchemaModel) :
    data_hash : str
    data : List[WantedFullData]

class ListOfWantedDataResponse(BaseSchemaModel) :
    data_hash : str
    data : List[WantedFullData]

class CheckHashResponse(BaseSchemaModel) :
    data_hash : str
    status : str = Field(default = 'OK')

    @validator('status')
    @classmethod
    def status_check(cls, v) :
        assert v in ['OK', 'Expired'], ValueError('Invaild Status')
        return v
    
class VideoPathRequest(BaseSchemaModel) :
    id : int
    video : Optional[str]
    video_source : Optional[str]

    is_err : bool = Field(default = False)
    err_msg : Optional[str] = Field(default = '')

class VideoPathResponse(BaseSchemaModel) :
    id : int
    video : str
    checksum : str = Field(default = 'OK')

    @validator('checksum')
    @classmethod
    def checksum_check(cls, v) :
        assert v in ['OK', 'INVALID'], ValueError('Invaild Status')
        return v