from sqlalchemy import Column, Integer, String
from database import Base

class Tourist(Base):
    __tablename__ = "tourists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    contact = Column(String)
    visitor_type = Column(String)
    nationality = Column(String)

class Transit(Base):
    __tablename__ = "transit_visitors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    contact = Column(String)
    vehicle_reg = Column(String)
    visitor_type = Column(String)
    nationality = Column(String)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    school = Column(String)
    institution = Column(String)
    contact = Column(String)
    visitor_type = Column(String)
    nationality = Column(String)