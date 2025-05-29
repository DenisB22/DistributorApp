from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app import commons
from app.db.database import get_mssql_db
from app.models import UserMapping
from app.schemas.partners import PartnerResponse
from app.utils import get_current_user_with_mapping

router = APIRouter(prefix="/microinvest/partners", tags=["Microinvest - Partners"])

# TODO: Add correct format of ResponseModel
@router.get("/")
def get_partners(
    mssql_db: Session = Depends(get_mssql_db),
    current_user_mapping: UserMapping = Depends(get_current_user_with_mapping),
    page: int = Query(1, alias="page", ge=1),
    limit: int = Query(20, le=100, description="Number of results per page (max 100)"),
    id: int = Query(None, alias="id"),
    company: str = Query(None, alias="company"),
    mol: str = Query(None, alias="mol"),
    phone: str = Query(None, alias="phone"),
    taxno: str = Query(None, alias="taxno")
):
    """Returns a paginated list of partners with optional filters."""
    
    # Base SQL Query
    query = """
        SELECT 
            p.ID AS partner_id,
            p.Code AS partner_code,
            COALESCE(p.Company, p.Company2) AS company,
            COALESCE(p.MOL, p.MOL2) AS mol,
            COALESCE(p.City, p.City2) AS city,
            COALESCE(p.Address, p.Address2) AS address,
            COALESCE(p.Phone, p.Phone2) AS phone,
            p.Fax AS fax,
            p.eMail AS email,
            p.TaxNo AS tax_no,
            p.Bulstat AS bulstat,
            p.BankName AS bank_name,
            p.BankCode AS bank_code,
            p.BankAcct AS bank_acct,
            p.BankVATName AS bank_vat_name,
            p.BankVATCode AS bank_vat_code,
            p.BankVATAcct AS bank_vat_acct,
            p.PriceGroup AS price_group,
            p.Discount AS discount,
            p.Type AS type,
            p.IsVeryUsed AS is_very_used,
            p.UserID AS user_id,
            p.GroupID AS group_id,
            p.UserRealTime AS user_real_time,
            p.Deleted AS deleted,
            p.CardNumber AS card_number,
            COALESCE(p.Note1, p.Note2) AS note,
            p.PaymentDays AS payment_days
        FROM dbo.Partners p WHERE 1=1
    """
    
    # Add filters dynamically
    params = {}
    if id:
        query += " AND ID = :id"
        params["id"] = id
    if company:
        query += " AND Company LIKE :company"
        params["company"] = f"%{company}%"  # Search by company name
    if mol:
        query += " AND MOL LIKE :mol"
        params["mol"] = f"%{mol}%"
    if phone:
        query += " AND Phone LIKE :phone"
        params["phone"] = f"%{phone}%"
    if taxno:
        query += " AND TaxNO = :taxno"
        params["taxno"] = taxno

    # Add limit and offset for pagination
    offset = (page - 1) * limit
    
    query += " ORDER BY ID OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY"
    params["offset"] = offset
    params["limit"] = limit

    try:
        # Execute query
        partners = mssql_db.execute(text(query), params).mappings().all()

        return {
            "page": page,
            "limit": limit,
            "total_records": len(partners),
            "partners": [
                PartnerResponse(
                    partner_id=row.partner_id,
                    partner_code=row.partner_code,
                    company=row.company,
                    mol=row.mol,
                    city=row.city,
                    address=row.address,
                    phone=row.phone,
                    fax=row.fax,
                    email=row.email,
                    tax_no=row.tax_no,
                    bulstat=row.bulstat,
                    bank_name=row.bank_name,
                    bank_code=row.bank_code,
                    bank_acct=row.bank_acct,
                    bank_vat_name=row.bank_vat_name,
                    bank_vat_code=row.bank_vat_code,
                    bank_vat_acct=row.bank_vat_acct,
                    price_group=row.price_group,
                    discount=row.discount,
                    type=row.type,
                    is_very_used=row.is_very_used,
                    user_id=row.user_id,
                    group_id=row.group_id,
                    user_real_time=row.user_real_time,
                    deleted=row.deleted,
                    card_number=row.card_number,
                    note=row.note,
                    payment_days=row.payment_days
                )
                for row in partners
            ]
        }

    except Exception as e:
        return commons.return_http_400_response(f'An error occurred: {e}')