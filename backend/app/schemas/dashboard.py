from pydantic import BaseModel
from typing import Optional
from app.schemas.operations import OperationResponse


class TopEntity(BaseModel):
    name: str
    value: float | int


class DashboardResponse(BaseModel):
    total_sales: int
    total_quantity: float
    total_revenue: float
    top_partner: Optional[TopEntity]
    top_good: Optional[TopEntity]
    recent_operations: list[OperationResponse]