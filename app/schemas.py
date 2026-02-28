from pydantic import BaseModel, EmailStr
from datetime import date


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    department: str | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    department: str | None

    class Config:
        orm_mode = True


 

class WellnessCreate(BaseModel):
    work_hours: float
    fatigue_score: int
    stress_level: int
    sleep_hours: float
    productivity_score: int

class WellnessResponse(WellnessCreate):
    id: int
    employee_id: int
    date: date

    class Config:
        orm_mode = True