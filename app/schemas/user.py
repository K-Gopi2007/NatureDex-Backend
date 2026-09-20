from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    profile_picture: Optional[str] = None
    xp: int
    level: int
    total_discoveries: int
    created_at: datetime

    class Config:
        from_attributes = True
