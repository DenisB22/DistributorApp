from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.schemas.operations import OperationResponse
from app.db.database import get_mssql_db
from app.utils import get_current_user_with_mapping
from app.commons import validate_start_date_before_end_date, is_superuser_based_on_user_level
from app.models import UserMapping
from typing import Optional

router = APIRouter(prefix="/microinvest/operations", tags=["Microinvest - Operations"])

@router.get("/", response_model=list[OperationResponse], response_model_exclude_none=True)
def get_operations(
    db: Session = Depends(get_mssql_db),
    current_user_mapping: UserMapping = Depends(get_current_user_with_mapping),
    user_id: Optional[int] = Query(None, description="Filter by User ID"),
    partner_id: Optional[int] = Query(None, description="Filter by Partner ID"),
    good_id: Optional[int] = Query(None, description="Filter by Good ID"),
    oper_type: Optional[int] = Query(None, description="Filter by Operation Type"),
    start_date: Optional[str] = Query(None, description="Filter from Date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Filter to Date (YYYY-MM-DD)"),
    limit: int = Query(50, description="Limit the number of results", gt=0),
    offset: int = Query(0, description="Offset for pagination", ge=0)
):
    """
    Retrieves operations (sales/purchases) from Microinvest.
    - If the user is an admin, they get all operations.
    - If the user is not an admin, they only get their own operations.
    - Supports filtering by user (Only for admin/staff), partner, good, operation type, and date range.
    - Supports pagination.
    """

    query = """
        SELECT  
            u.Name AS user_name,
            p.Company AS partner_name, 
            GoodID AS good_id,
            g.Name AS good_name, 
            ot.BG AS operation_name,
            o.ID AS operation_id,
            o.OperType AS operation_type,
            o.UserID AS user_id,
            o.PartnerID AS partner_id,
            o.Date AS operation_date, 
            o.Qtty AS operation_qtty, 
            o.PriceOut AS price_out, 
            o.PriceIn AS price_in
        FROM dbo.Operations o
        LEFT JOIN dbo.Users u ON o.UserID = u.ID
        LEFT JOIN dbo.Partners p ON o.PartnerID = p.ID
        LEFT JOIN dbo.Goods g ON o.GoodID = g.ID
        LEFT JOIN dbo.OperationType ot ON o.OperType = ot.ID
        WHERE 1=1
        AND ot.BG IS NOT NULL
    """
    params = {}

    # Validate start date is before end date
    if start_date and end_date:
        validate_start_date_before_end_date(start_date, end_date)
        
    # Apply filtering for non-admin users
    if not is_superuser_based_on_user_level(current_user_mapping.user_level):
        query += " AND o.UserID = :current_user_id"
        params["current_user_id"] = current_user_mapping.microinvest_user_id

    # Apply filters
    if user_id and is_superuser_based_on_user_level(current_user_mapping.user_level):
        query += " AND o.UserID = :user_id"
        params["user_id"] = user_id
    if partner_id:
        query += " AND o.PartnerID = :partner_id"
        params["partner_id"] = partner_id
    if good_id:
        query += " AND o.GoodID = :good_id"
        params["good_id"] = good_id
    if oper_type:
        query += " AND o.OperType = :oper_type"
        params["oper_type"] = oper_type
    if start_date:
        query += " AND o.Date >= :start_date"
        params["start_date"] = start_date
    if end_date:
        query += " AND o.Date <= :end_date"
        params["end_date"] = end_date

    # # Add pagination
    query += " ORDER BY Date DESC OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY"
    params["limit"] = limit
    params["offset"] = offset
    result = db.execute(text(query), params)
    operations = result.fetchall()

    # Convert query results to response model
    return [
        OperationResponse(
            operation_id=row.operation_id,
            operation_type=row.operation_type,
            operation_name=row.operation_name,
            operation_date=row.operation_date,
            operation_qtty=row.operation_qtty,
            user_id=row.user_id,
            user_name=row.user_name,
            partner_id=row.partner_id,
            partner_name=row.partner_name,
            good_id=row.good_id,
            good_name=row.good_name,
            price_out=row.price_out,
            price_in=row.price_in if is_superuser_based_on_user_level(current_user_mapping.user_level) else None  # Hide PriceIn for non-admins
        )
        for row in operations
    ]
