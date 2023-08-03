from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from sqlalchemy import ForeignKey, Column
from sqlalchemy import (
    TEXT, Integer, String,
    REAL, Boolean, TIMESTAMP
)
from sqlalchemy.orm import relationship

from app.models.schemas.admin import CreateWantedDataRequest, UpdateWantedDataRequest
from app.db.repositories.base_class import Base

@dataclass
class Wanted(Base):
    __tablename__ = "wanted"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wanted_id = Column(Integer, nullable=True)
    name = Column(TEXT, nullable=True)
    sex = Column(Boolean, nullable=True) # True : Female, False : Male
    age = Column(REAL, nullable=True)
    wanted_type = Column(Boolean, nullable=False, default=False) # True : urgent case

    ## relationships
    detail = relationship("WantedDetail", back_populates="_wanted")
    datasource = relationship("WantedDataSource", back_populates="_wanted")
    requester = relationship("Requester", back_populates="_wanted")

    @classmethod #orm 객체로 변환
    def create(cls, request: CreateWantedDataRequest, id: Optional[int] = None) -> "Wanted":
        return  cls(
            wanted_id = request.wanted_id,
            name = request.name,
            sex = request.sex,
            age = request.age,
            wanted_type = request.wanted_type
        )
    
    @classmethod
    def convert_dict(cls, request: UpdateWantedDataRequest) :
        return {
            "id" : request.id,
            "wanted_id" : request.wanted_id,
            "name" : request.name,
            "sex" : request.sex,
            "age" : request.age,
            "wanted_type" : request.wanted_type
        }

@dataclass
class WantedDetail(Base):
    __tablename__ = "wanted_detail"

    id = Column(Integer, ForeignKey("wanted.id"), primary_key=True)
    height = Column(REAL, nullable = True)
    weight = Column(String(100), nullable = True)
    registered_address = Column(String(100), nullable=True)
    residence = Column(String(100), nullable=True)
    criminal = Column(String(50), nullable=True)
    relational_link = Column(TEXT, nullable=True)
    characteristic = Column(TEXT, nullable=True)
    started_at = Column(TIMESTAMP, nullable=True)
    ended_at = Column(TIMESTAMP, nullable=True)

    ## relationships
    _wanted = relationship("Wanted", back_populates="detail", uselist=False)
    
    @classmethod #orm 객체로 변환
    def create(cls, id, request: CreateWantedDataRequest) -> "WantedDetail":
        return cls(
            id = id,
            height = request.height,
            weight = request.weight,
            registered_address = request.registered_address,
            residence = request.residence,
            criminal = request.criminal,
            relational_link = request.relational_link,
            characteristic = request.characteristic,
            started_at = request.started_at.replace(tzinfo=None),
            ended_at = request.ended_at.replace(tzinfo=None)
        )
    
    @classmethod
    def convert_dict(cls, request : UpdateWantedDataRequest) :
        return {
            "id" : request.id,
            "height" : request.height,
            "weight" : request.weight,
            "registered_address" : request.registered_address,
            "residence" : request.residence,
            "criminal" : request.criminal,
            "relational_link" : request.relational_link,
            "characteristic" : request.characteristic,
            "started_at" : request.started_at.replace(tzinfo=None),
            "ended_at" : request.ended_at.replace(tzinfo=None)

        }

@dataclass
class WantedDataSource(Base) :
    __tablename__ = "wanted_data_source"

    id = Column(Integer, ForeignKey("wanted.id"), primary_key=True)
    image = Column(TEXT, nullable=True)
    video = Column(TEXT, nullable=True)
    generated = Column(Integer, default=0, nullable = True)
    driving_video = Column(TEXT, nullable=True)
    error_msg = Column(TEXT, nullable=True)

    ## relationships
    _wanted = relationship("Wanted", back_populates="datasource", uselist=False)

    @classmethod
    def create(cls, id: int, image_path: str) -> "WantedDataSource":
        return cls(
            id = id,
            image = image_path
        )
