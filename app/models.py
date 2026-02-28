
from .database import Base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Date
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
from datetime import date


 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
     
    department = Column(String, nullable=True)
    role = Column(String, default="EMPLOYEE", nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    company = relationship("Company", backref="users")



class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())




class WellnessRecord(Base):
    __tablename__ = "wellness_records"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, default=date.today)

    work_hours = Column(Float)
    fatigue_score = Column(Integer)        # 1-10
    stress_level = Column(Integer)         # 1-10
    sleep_hours = Column(Float)
    productivity_score = Column(Integer)   # 1-10

    employee = relationship("User")