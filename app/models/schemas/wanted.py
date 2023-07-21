from typing import Optional, List
from pydantic import BaseModel
from app.models.domain.wanted import WantedData

class WantedDataResponse(BaseModel) :
    data_hash : str
    data : List[WantedData]

class ListOfWantedDataResponse(BaseModel) :
    data_hash : str
    data : List[WantedData]

class OptionalListOfWantedDataResponse(BaseModel) :
    data_hash : str
    data : Optional[List[WantedData]]
