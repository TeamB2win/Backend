from pydantic import BaseModel
from typing import List
from typing import Optional


class CreateCriminalDataRequest(BaseModel):
    registered_address: str
    residence: str
    wanted_type: int
    name: str
    criminal: str
    relational_link: str
    characteristic: str
    image: bytes
    video_url: str


class CriminalDataSchema(BaseModel):
    id: Optional[int]
    registered_address: str
    residence: str
    wanted_type: int
    name: str
    criminal: str
    relational_link: str
    characteristic: str
    image: bytes
    video_url: bytes

    class Config:
        from_attributes = True


class ListCriminalDataResponse(BaseModel):
    CriminalData: List[CriminalDataSchema]
