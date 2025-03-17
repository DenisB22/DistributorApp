from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.db.database import get_mssql_db

router = APIRouter(prefix="/microinvest/partners", tags=["Microinvest - Partners"])


@router.get("/")
def get_partners(
    mssql_db: Session = Depends(get_mssql_db),
    page: int = Query(1, alias="page", ge=1),
    limit: int = Query(50, alias="limit", ge=1, le=100),
    id: int = Query(None, alias="id"),
    company: str = Query(None, alias="company"),
    mol: str = Query(None, alias="mol"),
    phone: str = Query(None, alias="phone"),
    taxno: str = Query(None, alias="taxno")
):
    """Returns a paginated list of partners with optional filters."""
    
    # Base SQL Query
    query = "SELECT * FROM dbo.Partners WHERE 1=1"
    
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

    # Execute query
    result = mssql_db.execute(text(query), params).mappings().all()
    
    # Transform result into list of dictionaries
    partners = [dict(row) for row in result]

    return {"partners": partners, "page": page, "limit": limit}