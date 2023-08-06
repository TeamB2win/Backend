from typing import Optional, List, Union
from datetime import datetime
from fastapi import File
from pydantic import HttpUrl, Field

from app.models.domain.base import BaseDomainModel

class WantedDetailData(BaseDomainModel) :
    height : Optional[int] = None
    weight : Optional[str] = None
    registered_address : Optional[str] = None
    residence : Optional[str] = None
    criminal : Optional[str] = None
    relational_link : Optional[str] = None
    characteristic : Optional[str] = None
    started_at : datetime
    ended_at : datetime
    
class WantedSourceData(BaseDomainModel) :
    image : str
    video : Optional[str] = None
    generated : int
    driving_video : Optional[str] = None
    error_msg : Optional[str] = None
    
class WantedFullData(BaseDomainModel) :
    id : int
    wanted_id : Optional[int] = None
    name : Optional[str] = None
    sex : bool
    age : Optional[int] = None
    wanted_type : bool

    detail : List[WantedDetailData]
    datasource : List[WantedSourceData]