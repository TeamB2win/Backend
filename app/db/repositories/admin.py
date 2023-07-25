from sqlalchemy import ForeignKey, Column
from sqlalchemy import Integer, VARCHAR, Sequence

from sqlalchemy.orm import relationship
from app.db.repositories.base_class import Base

class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, Sequence('admin_id_seq'), primary_key=True)
    admin_id = Column(VARCHAR, nullable=False, primary_key=True)
    password = Column(VARCHAR, nullable=False)
    age = Column(Integer, nullable=True)

    ## relationships
    detail = relationship("AdminDetail", back_populates="_admin")
    requester = relationship("Requester", back_populates="_admin")

class AdminDetail(Base):
    __tablename__ = "admin_detail"

    id = Column(Integer, ForeignKey("admin.id"))
    name = Column(VARCHAR, nullable=True)
    position = Column(VARCHAR, nullable=True)
    work_place = Column(VARCHAR, nullable=True)

    ## relationships
    _admin = relationship("Admin", back_populates="detail")


class Requester(Base) :
    __tablename__ = "requester"

    id = Column(Integer, ForeignKey("wanted.id"))
    admin_id = Column(Integer, ForeignKey("admin.id"))
    requester = Column(VARCHAR)
    name = Column(VARCHAR)
    position = Column(VARCHAR)

    ## relationships
    _wanted = relationship("Wanted", back_populates="requester")
    _admin = relationship("Admin", back_populates="requester")