from typing import Optional, List
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
    data : Optional[List[WantedFullData]]
