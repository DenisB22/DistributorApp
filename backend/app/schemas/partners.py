from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class PartnerResponse(BaseModel):
    partner_id: int
    partner_code: Optional[str] = None
    company: Optional[str] = None
    mol: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    tax_no: Optional[str] = None
    bulstat: Optional[str] = None
    bank_name: Optional[str] = None
    bank_code: Optional[str] = None
    bank_acct: Optional[str] = None
    bank_vat_name: Optional[str] = None
    bank_vat_code: Optional[str] = None
    bank_vat_acct: Optional[str] = None
    price_group: Optional[int] = None
    discount: Optional[float] = None
    type: Optional[int] = None
    is_very_used: Optional[int] = None
    user_id: Optional[int] = None
    group_id: Optional[int] = None
    user_real_time: Optional[datetime] = None
    deleted: Optional[int] = None
    card_number: Optional[str] = None
    note: Optional[str] = None
    payment_days: Optional[int] = None

    class Config:
        orm_mode = True
