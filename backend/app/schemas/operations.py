from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OperationResponse(BaseModel):
    operation_id: int
    operation_type: int
    operation_name: str
    operation_date: datetime
    operation_qtty: float
    user_id: int
    user_name: str
    partner_id: int
    partner_name: str
    good_id: int
    good_name: str
    price_out: float  # Always visible
    price_in: Optional[float] = None  # Only visible to admins


    class Config:
        orm_mode = True