from typing import Optional, List
from datetime import datetime
from fastapi import File
from pydantic import BaseModel, HttpUrl

from app.models.domain.base import BaseDomainModel

class WantedData(BaseDomainModel) :
    id : int
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