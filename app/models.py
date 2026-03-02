
from .database import Base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Date
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
from datetime import date
from sqlalchemy import UniqueConstraint
 

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

    __table_args__ = (
        UniqueConstraint("employee_id", "date", name="unique_employee_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, default=date.today)

    work_hours = Column(Float)
    fatigue_score = Column(Integer)
    stress_level = Column(Integer)
    sleep_hours = Column(Float)
    productivity_score = Column(Integer)

    employee = relationship("User")