from pydantic import BaseModel


class UserMappingBase(BaseModel):
    user_id: int  # ID from PostgreSQL Users table
    microinvest_user_id: int  # ID from Microinvest Users table

class UserMappingCreate(UserMappingBase):
    """Schema for creating a new user mapping"""
    pass  # No extra fields needed for creation

class UserMappingResponse(UserMappingBase):
    """Schema for returning user mapping details"""
    id: int
    user_level: int  # UserLevel from Microinvest

    class Config:
        orm_mode = True  # Enables ORM serialization