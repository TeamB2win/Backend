from sqlalchemy import ForeignKey, Column
from sqlalchemy import (
    TEXT, Integer, String,
    REAL, Sequence, Boolean,
    TIMESTAMP
)
from sqlalchemy.orm import relationship

from app.db.repositories.base_class import Base

class Wanted(Base):
    __tablename__ = "wanted"

    id = Column(Integer, Sequence('wanted_id_seq'), primary_key=True)
    name = Column(TEXT, nullable=True)
    sex = Column(Boolean, nullable=True) # True : Female, False : Male
    age = Column(Integer, nullable=True)
    wanted_type = Column(Boolean, nullable=False, default=False) # True : urgent case

    ## relationships
    detail = relationship("WantedDetail", back_populates="_wanted")
    datasource = relationship("WantedDataSource", back_populates="_wanted")
    requester = relationship("Requester", back_populates="_wanted")

class WantedDetail(Base):
    __tablename__ = "wanted_detail"

    id = Column(Integer, ForeignKey("wanted.id"), primary_key=True)
    height = Column(REAL, nullable = True, default=170)
    weight = Column(String(100), nullable = True, default="왜소한 체격")
    registered_address = Column(String(100), nullable=True)
    residence = Column(String(100), nullable=True)
    criminal = Column(String(50), nullable=True)
    relational_link = Column(TEXT, nullable=True)
    characteristic = Column(TEXT, nullable=True)
    started_at = Column(TIMESTAMP, nullable=True)
    ended_at = Column(TIMESTAMP, nullable=True)

    ## relationships
    _wanted = relationship("Wanted", back_populates="detail", uselist=False)

class WantedDataSource(Base) :
    __tablename__ = "wanted_data_source"

    id = Column(Integer, ForeignKey("wanted.id"), primary_key=True)
    image = Column(TEXT, nullable=True)
    video = Column(TEXT, nullable=True)
    generated = Column(Integer, default=0, nullable = False)

    ## relationships
    _wanted = relationship("Wanted", back_populates="datasource", uselist=False)