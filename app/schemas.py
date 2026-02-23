from pydantic import BaseModel, EmailStr

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
