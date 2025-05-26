from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OperationResponse(BaseModel):
    operation_id: int
    operation_type: Optional[int] = None
    operation_name: Optional[str] = None
    operation_date: Optional[datetime] = None
    operation_qtty: Optional[float] = None
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    partner_id: Optional[int] = None
    partner_name: Optional[str] = None
    good_id: Optional[int] = None
    good_name: Optional[str] = None
    price_out: Optional[float] = None  # Always visible
    price_in: Optional[float] = None  # Only visible to admins

    class Config:
        orm_mode = True
