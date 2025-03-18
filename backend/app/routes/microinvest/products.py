from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.database import get_mssql_db
from app.schemas.user_mapping import UserMappingResponse
from app.utils import get_current_user_with_mapping

router = APIRouter(prefix="/microinvest/products", tags=["Microinvest - Products"])


@router.get("/")
def get_products(
    mssql_db: Session = Depends(get_mssql_db),
    name: str = Query(None, description="Filter by product name"),
    barcode: str = Query(None, description="Filter by barcode"),
    page: int = Query(1, ge=1, description="Page number (1-based index)"),
    page_size: int = Query(20, le=100, description="Number of results per page (max 100)"),
):
    """Returns a paginated list of products from Microinvest"""

    offset = (page - 1) * page_size  # Calculates where to start next page from

    query = text(
        f"""
        SELECT * FROM dbo.Goods
        WHERE 1=1
        """
    )

    if name:
        query = text(f"{query.text} AND Name LIKE :name")
    if barcode:
        query = text(f"{query.text} AND BarCode1 = :barcode")

    # Add Pagination
    query = text(f"{query.text} ORDER BY ID OFFSET :offset ROWS FETCH NEXT :page_size ROWS ONLY")

    result = mssql_db.execute(query, {
        "name": f"%{name}%" if name else None,
        "barcode": barcode,
        "offset": offset,
        "page_size": page_size
    }).mappings().all()

    return {
        "page": page,
        "page_size": page_size,
        "total_records": len(result),
        "products": result
    }