from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Request model for user login
class LoginRequest(BaseModel):
    email: str
    password: str


# Base user model (shared fields between different schemas)
class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    is_superuser: bool = False
    is_active: bool = True

    class Config:
        orm_mode = True


# Schema for creating a new user (adds password field)
class UserCreate(UserBase):
    password: str


# Schema for updating user details (all fields optional)
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_superuser: Optional[bool] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True


# Schema for returning user data (adds database fields)
class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


