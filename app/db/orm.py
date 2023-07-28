from sqlalchemy import Boolean, Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base

from models.schemas.admin import CreateCriminalDataRequest

Base = declarative_base()


class CriminalData(Base):
    __tablename__ = "criminal_data"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    wanted_type = Column(Integer)
    criminal = Column(String(256))
    registered_address = Column(String(256))
    residence = Column(String(256))
    characteristic = Column(String(256))
    relational_link = Column(String(256))
    image = Column(LargeBinary) #LargeBinary
    # video_url = Column(LargeBinary) #LargeBinary

    
    @classmethod #orm 객체로 변환
    def create(cls, request: CreateCriminalDataRequest) -> "CriminalData":
        return cls(
            name=request.name,
            wanted_type=request.wanted_type,
            criminal=request.criminal,
            registered_address=request.registered_address,
            residence=request.residence,
            characteristic=request.characteristic,
            relational_link=request.relational_link,
            image=request.image,
            #video_url=request.video_url
        )
from sqlalchemy import Boolean, Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base

from models.schemas.admin import CreateCriminalDataRequest

Base = declarative_base()


class CriminalData(Base):
    __tablename__ = "criminal_data"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    wanted_type = Column(Integer)
    criminal = Column(String(256))
    registered_address = Column(String(256))
    residence = Column(String(256))
    characteristic = Column(String(256))
    relational_link = Column(String(256))
    image = Column(LargeBinary) #LargeBinary
    # video_url = Column(LargeBinary) #LargeBinary

    
    @classmethod #orm 객체로 변환
    def create(cls, request: CreateCriminalDataRequest) -> "CriminalData":
        return cls(
            name=request.name,
            wanted_type=request.wanted_type,
            criminal=request.criminal,
            registered_address=request.registered_address,
            residence=request.residence,
            characteristic=request.characteristic,
            relational_link=request.relational_link,
            image=request.image,
            #video_url=request.video_url
        )
from sqlalchemy import Boolean, Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base

from models.schemas.admin import CreateCriminalDataRequest

Base = declarative_base()


class CriminalData(Base):
    __tablename__ = "criminal_data"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    wanted_type = Column(Integer)
    criminal = Column(String(256))
    registered_address = Column(String(256))
    residence = Column(String(256))
    characteristic = Column(String(256))
    relational_link = Column(String(256))
    image = Column(LargeBinary) #LargeBinary
    # video_url = Column(LargeBinary) #LargeBinary

    
    @classmethod #orm 객체로 변환
    def create(cls, request: CreateCriminalDataRequest) -> "CriminalData":
        return cls(
            name=request.name,
            wanted_type=request.wanted_type,
            criminal=request.criminal,
            registered_address=request.registered_address,
            residence=request.residence,
            characteristic=request.characteristic,
            relational_link=request.relational_link,
            image=request.image,
            #video_url=request.video_url
        )
from sqlalchemy import Boolean, Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base

from models.schemas.admin import CreateCriminalDataRequest

Base = declarative_base()


class CriminalData(Base):
    __tablename__ = "criminal_data"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    wanted_type = Column(Integer)
    criminal = Column(String(256))
    registered_address = Column(String(256))
    residence = Column(String(256))
    characteristic = Column(String(256))
    relational_link = Column(String(256))
    image = Column(LargeBinary) #LargeBinary
    # video_url = Column(LargeBinary) #LargeBinary

    
    @classmethod #orm 객체로 변환
    def create(cls, request: CreateCriminalDataRequest) -> "CriminalData":
        return cls(
            name=request.name,
            wanted_type=request.wanted_type,
            criminal=request.criminal,
            registered_address=request.registered_address,
            residence=request.residence,
            characteristic=request.characteristic,
            relational_link=request.relational_link,
            image=request.image,
            #video_url=request.video_url
        )
from sqlalchemy import Boolean, Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base

from models.schemas.admin import CreateCriminalDataRequest

Base = declarative_base()


class CriminalData(Base):
    __tablename__ = "criminal_data"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    wanted_type = Column(Integer)
    criminal = Column(String(256))
    registered_address = Column(String(256))
    residence = Column(String(256))
    characteristic = Column(String(256))
    relational_link = Column(String(256))
    image = Column(LargeBinary) #LargeBinary
    # video_url = Column(LargeBinary) #LargeBinary

    
    @classmethod #orm 객체로 변환
    def create(cls, request: CreateCriminalDataRequest) -> "CriminalData":
        return cls(
            name=request.name,
            wanted_type=request.wanted_type,
            criminal=request.criminal,
            registered_address=request.registered_address,
            residence=request.residence,
            characteristic=request.characteristic,
            relational_link=request.relational_link,
            image=request.image,
            #video_url=request.video_url
        )
from sqlalchemy import Boolean, Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base

from models.schemas.admin import CreateCriminalDataRequest

Base = declarative_base()


class CriminalData(Base):
    __tablename__ = "criminal_data"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    wanted_type = Column(Integer)
    criminal = Column(String(256))
    registered_address = Column(String(256))
    residence = Column(String(256))
    characteristic = Column(String(256))
    relational_link = Column(String(256))
    image = Column(LargeBinary) #LargeBinary
    # video_url = Column(LargeBinary) #LargeBinary

    
    @classmethod #orm 객체로 변환
    def create(cls, request: CreateCriminalDataRequest) -> "CriminalData":
        return cls(
            name=request.name,
            wanted_type=request.wanted_type,
            criminal=request.criminal,
            registered_address=request.registered_address,
            residence=request.residence,
            characteristic=request.characteristic,
            relational_link=request.relational_link,
            image=request.image,
            #video_url=request.video_url
        )
from sqlalchemy import Boolean, Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base

from models.schemas.admin import CreateCriminalDataRequest

Base = declarative_base()


class CriminalData(Base):
    __tablename__ = "criminal_data"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    wanted_type = Column(Integer)
    criminal = Column(String(256))
    registered_address = Column(String(256))
    residence = Column(String(256))
    characteristic = Column(String(256))
    relational_link = Column(String(256))
    image = Column(LargeBinary) #LargeBinary
    # video_url = Column(LargeBinary) #LargeBinary

    
    @classmethod #orm 객체로 변환
    def create(cls, request: CreateCriminalDataRequest) -> "CriminalData":
        return cls(
            name=request.name,
            wanted_type=request.wanted_type,
            criminal=request.criminal,
            registered_address=request.registered_address,
            residence=request.residence,
            characteristic=request.characteristic,
            relational_link=request.relational_link,
            image=request.image,
            #video_url=request.video_url
        )
