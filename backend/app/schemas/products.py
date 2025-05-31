from pydantic import BaseModel
from typing import Optional, List


class ProductResponse(BaseModel):
    product_id: int
    code: Optional[str] = None
    bar_code: Optional[str] = None
    catalog: Optional[str] = None
    name: Optional[str] = None
    measure: Optional[str] = None
    ratio: Optional[float] = None
    price_in: Optional[float] = None  # Only visible to admins
    price_out: Optional[float] = None  # Always visible
    min_qtty: Optional[float] = None
    normal_qtty: Optional[float] = None
    description: Optional[str] = None
    type: Optional[int] = None
    is_recipe: Optional[int] = None
    tax_group: Optional[int] = None
    is_very_used: Optional[int] = None
    group_id: Optional[int] = None
    deleted: Optional[int] = None

    class Config:
        orm_mode = True


class ProductApiResponse(BaseModel):
    page: int
    page_size: int
    total_records: int
    products: Optional[List[ProductResponse]]
