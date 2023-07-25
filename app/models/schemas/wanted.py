from typing import Optional, List
from app.models.schemas.base import BaseSchemaModel
from app.models.domain.wanted import WantedData

class WantedDataResponse(BaseSchemaModel) :
    data_hash : str
    data : List[WantedData]

class ListOfWantedDataResponse(BaseSchemaModel) :
    data_hash : str
    data : List[WantedData]

class OptionalListOfWantedDataResponse(BaseSchemaModel) :
    data_hash : str
    data : Optional[List[WantedData]]
