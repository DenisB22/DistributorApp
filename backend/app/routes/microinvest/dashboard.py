from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.schemas.operations import OperationResponse
from app.schemas.dashboard import DashboardResponse, TopEntity
from app.db.database import get_mssql_db
from app.utils import get_current_user_with_mapping
from app.commons import validate_start_date_before_end_date, is_superuser_based_on_user_level
from app.models import UserMapping
from app.enums.operations import OperationTypeID
from typing import Optional
from datetime import datetime, timedelta


router = APIRouter(prefix="/microinvest/dashboard", tags=["Microinvest - Dashboard"])


def resolve_period(period: str, start_date: Optional[str], end_date: Optional[str]) -> tuple[str, str]:
    end_date = datetime(2024, 10, 1, 23, 59, 59)
    if period == "7d":
        return str(end_date - timedelta(days=7)), str(end_date)
    elif period == "3m":
        return str(end_date - timedelta(days=90)), str(end_date)
    elif period == "1y":
        return str(end_date - timedelta(days=365)), str(end_date)
    elif period == "custom" and start_date and end_date:
        return start_date, end_date
    else:
        return str(end_date - timedelta(days=7)), str(end_date)


@router.get("/", response_model=DashboardResponse)
def get_dashboard_data(
    db: Session = Depends(get_mssql_db),
    current_user_mapping: UserMapping = Depends(get_current_user_with_mapping),
    period: Optional[str] = Query("7d", description="Period filter: '7d', '3m', '1y', or 'custom'"),
    start_date: Optional[str] = Query(None, description="Custom start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Custom end date (YYYY-MM-DD)")
):
    validate_start_date_before_end_date(start_date, end_date)
    
    resolved_start, resolved_end = resolve_period(period, start_date, end_date)

    is_staff = is_superuser_based_on_user_level(current_user_mapping.user_level)
    user_filter = "" if is_staff else "AND o.UserID = :user_id"

    params = {
        "start_date": resolved_start,
        "end_date": resolved_end,
        "user_id": current_user_mapping.microinvest_user_id,
        "operation_type": OperationTypeID.SALE
    }

    # Total sales, quantity and revenue
    totals_query = f"""
        SELECT 
            COUNT(*) AS total_sales,
            SUM(o.Qtty) AS total_quantity,
            SUM(o.PriceOut * o.Qtty) AS total_revenue
        FROM dbo.Operations o
        WHERE o.OperType = 2
        AND o.Date BETWEEN :start_date AND :end_date
        {user_filter}
    """
    totals_result = db.execute(text(totals_query), params).mappings().first()

    # Top partner
    top_partner_query = f"""
        SELECT TOP 1 p.ID, p.Company, SUM(o.PriceOut * o.Qtty) AS total
        FROM dbo.Operations o
        JOIN dbo.Partners p ON o.PartnerID = p.ID
        WHERE o.OperType = :operation_type AND o.Date BETWEEN :start_date AND :end_date
        {user_filter}
        GROUP BY p.ID, p.Company
        ORDER BY total DESC
    """
    top_partner = db.execute(text(top_partner_query), params).mappings().first()

    # Top good
    top_good_query = f"""
        SELECT TOP 1 g.ID, g.Name, SUM(o.PriceOut * o.Qtty) AS total
        FROM dbo.Operations o
        JOIN dbo.Goods g ON o.GoodID = g.ID
        WHERE o.OperType = :operation_type AND o.Date BETWEEN :start_date AND :end_date
        {user_filter}
        GROUP BY g.ID, g.Name
        ORDER BY total DESC
    """
    top_good = db.execute(text(top_good_query), params).mappings().first()

    # Recent operations
    recent_query = f"""
        SELECT TOP 5 
            o.ID AS operation_id,
            o.OperType AS operation_type,
            o.Date AS operation_date,
            o.Qtty AS operation_qtty,
            o.PriceOut AS price_out,
            o.PriceIn AS price_in,
            ot.BG AS operation_name,
            g.Name AS good_name,
            g.ID AS good_id,
            p.Company AS partner_name,
            p.ID AS partner_id,
            o.UserID AS user_id,
            u.Name AS user_name
        FROM dbo.Operations o
        LEFT JOIN dbo.OperationType ot ON o.OperType = ot.ID
        LEFT JOIN dbo.Goods g ON o.GoodID = g.ID
        LEFT JOIN dbo.Partners p ON o.PartnerID = p.ID
        LEFT JOIN dbo.Users u ON o.UserID = u.ID
        WHERE o.OperType = :operation_type
        AND o.Date BETWEEN :start_date AND :end_date
        {user_filter}
        ORDER BY o.Date DESC
    """
    recent_result = db.execute(text(recent_query), params).mappings().all()
    recent_operations = [
        OperationResponse(
            operation_id=row.operation_id,
            operation_type=row.operation_type,
            operation_name=row.operation_name,  # Static for now
            operation_date=row.operation_date,
            operation_qtty=row.operation_qtty,
            user_id=row.user_id,
            user_name=row.user_name,
            partner_id=row.partner_id,
            partner_name=row.partner_name,
            good_id=row.good_id,
            good_name=row.good_name,
            price_out=row.price_out,
            price_in=row.price_in if is_staff else None
        )
        for row in recent_result
    ]

    return DashboardResponse(
        total_sales=totals_result.total_sales or 0,
        total_quantity=totals_result.total_quantity or 0,
        total_revenue=totals_result.total_revenue or 0.0,
        top_partner=TopEntity(id=top_partner.ID, name=top_partner.Company, value=top_partner.total) if top_partner else None,
        top_good=TopEntity(id=top_good.ID, name=top_good.Name, value=top_good.total) if top_good else None,
        recent_operations=recent_operations
    )