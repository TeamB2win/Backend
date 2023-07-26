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

class OptionalListOfWantedDataResponse(BaseSchemaModel) :
    data_hash : str
    status : str = Field(default = 'OK')
    data : Optional[List[WantedFullData]] = None

    @validator('status')
    def status_check(cls, v) :
        assert v in ['OK', 'NEW_DATA'], ValueError('Invaild Status')
        return v