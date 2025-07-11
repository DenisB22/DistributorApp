from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import commons
from app.constants import OperationQueryParams
from app.schemas.operations import OperationApiResponse, OperationResponse
from app.db.database import get_mssql_db
from app.utils import get_current_user_with_mapping
from app.commons import validate_start_date_before_end_date, is_superuser_based_on_user_level
from app.models import UserMapping
from typing import Optional

router = APIRouter(prefix="/microinvest/operations", tags=["Microinvest - Operations"])


@router.get("/", response_model=OperationApiResponse, response_model_exclude_none=True)
def get_operations(
    db: Session = Depends(get_mssql_db),
    current_user_mapping: UserMapping = Depends(get_current_user_with_mapping),
    user_id: Optional[int] = Query(None, description="Filter by User ID"),
    partner_id: Optional[int] = Query(None, description="Filter by Partner ID"),
    partner_name: Optional[str] = Query(None, description="Filter by Partner Name"),
    good_id: Optional[int] = Query(None, description="Filter by Good ID"),
    good_name: Optional[str] = Query(None, description="Filter by Good Name"),
    oper_type: Optional[int] = Query(None, description="Filter by Operation Type"),
    oper_name: Optional[str] = Query(None, description="Filter by Operation Name"),
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

    if not any([oper_type, oper_name, good_id, good_name, partner_id, partner_name]):
        return commons.return_http_400_response(f"At least one query should be provided: {f', '.join(OperationQueryParams.values())}")

    # Apply filters
    if user_id and is_superuser_based_on_user_level(current_user_mapping.user_level):
        query += " AND o.UserID = :user_id"
        params["user_id"] = user_id
    if partner_id:
        query += " AND o.PartnerID = :partner_id"
        params["partner_id"] = partner_id
    if partner_name:
        query += " AND p.Company = :partner_name"
        params["partner_name"] = partner_name
    if good_id:
        query += " AND o.GoodID = :good_id"
        params["good_id"] = good_id
    if good_name:
        query += " AND g.Name= :good_name"
        params["good_name"] = good_name
    if oper_type:
        query += " AND o.OperType = :oper_type"
        params["oper_type"] = oper_type
    if oper_name:
        query += " AND ot.BG = :oper_name"
        params["oper_name"] = oper_name
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
    try:
        result = db.execute(text(query), params)
        operations = result.fetchall()

        # Convert query results to response model
        return {
            "page": offset,
            "limit": limit,
            "total_records": len(operations),
            "operations": [
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
        }

    except Exception as e:
        return commons.return_http_400_response(f'An error occurred: {e}')


@router.get("/{operation_id}", response_model=OperationResponse, response_model_exclude_none=True)
def get_operation_by_id(
    operation_id: int,
    db: Session = Depends(get_mssql_db),
    current_user_mapping: UserMapping = Depends(get_current_user_with_mapping),
):
    """
    Retrieves a single operation by ID.
    Non-admin users can only access their own operations.
    Admins can access all operations.
    """

    query = """
        SELECT  
            u.Name AS user_name,
            p.Company AS partner_name, 
            o.GoodID AS good_id,
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
        WHERE o.ID = :operation_id
    """

    params = {"operation_id": operation_id}
    result = db.execute(text(query), params)
    operation = result.fetchone()

    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found.")

    # If not admin, ensure user can only access their own operations
    if not is_superuser_based_on_user_level(current_user_mapping.user_level):
        if operation.user_id != current_user_mapping.microinvest_user_id:
            raise HTTPException(status_code=403, detail="You do not have permission to view this operation.")

    response = OperationResponse(
        operation_id=operation.operation_id,
        operation_type=operation.operation_type,
        operation_name=operation.operation_name,
        operation_date=operation.operation_date,
        operation_qtty=operation.operation_qtty,
        user_id=operation.user_id,
        user_name=operation.user_name,
        partner_id=operation.partner_id,
        partner_name=operation.partner_name,
        good_id=operation.good_id,
        good_name=operation.good_name,
        price_out=operation.price_out,
        price_in=operation.price_in if is_superuser_based_on_user_level(current_user_mapping.user_level) else None
    )

    return response
