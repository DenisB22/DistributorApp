from pydantic import BaseModel


class UserMappingCreate(BaseModel):
    user_id: int  # ID from PostgreSQL Users table
    microinvest_user_id: int  # ID from Microinvest Users table