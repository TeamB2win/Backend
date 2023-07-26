from sqlalchemy import Boolean, Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base

from Backend.app.models.schemas.admin import CreateCriminalDataRequest

Base = declarative_base()


class CriminalData(Base):
    __tablename__ = "criminal_data"
    
    id = Column(Integer, primary_key=True, index=True)
    registered_address = Column(String(256))
    residence = Column(String(256))
    wanted_type = Column(Integer)
    name = Column(String(256))
    criminal = Column(String(256))
    relational_link = Column(String(256))
    characteristic = Column(String(256))
    image = Column(LargeBinary) #LargeBinary
    video_url = Column(LargeBinary) #LargeBinary

    def __repr__(self):
        return f"CriminalData(id={self.id}, registered_address={self.registered_address}, residence={self.residence}, wanted_type={self.wanted_type},name={self.name},criminal={self.criminal},relational_link={self.relational_link},characteristic={self.characteristic},image={self.image},video_url={self.video_url} )"

    @classmethod #orm 객체로 변환
    def create(cls, request: CreateCriminalDataRequest) -> "CriminalData":
        return cls(
            registered_address=request.registered_address,
            residence=request.residence,
            wanted_type=request.wanted_type,
            name=request.name,
            criminal=request.criminal,
            relational_link=request.relational_link,
            characteristic=request.characteristic,
            image=request.image,
            video_url=request.video_url
        )
