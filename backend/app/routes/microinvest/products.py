from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.database import get_mssql_db

router = APIRouter(prefix="/microinvest/products", tags=["Microinvest - Products"])


@router.get("/")
def get_products(
    mssql_db: Session = Depends(get_mssql_db),
    name: str = Query(None, description="Filter by product name"),
    code: str = Query(None, description="Filter by code"),
    barcode: str = Query(None, description="Filter by barcode"),
    page: int = Query(1, ge=1, description="Page number (1-based index)"),
    page_size: int = Query(20, le=100, description="Number of results per page (max 100)"),
):
    """Returns a paginated list of products from Microinvest"""

    offset = (page - 1) * page_size  # Calculates where to start next page from

    query = text(f"""
        SELECT
            ID,
            Code,
            COALESCE(BarCode1, BarCode2, BarCode3) AS BarCode,
            COALESCE(Catalog1, Catalog2, Catalog3) AS Catalog,
            COALESCE(Name, Name2) AS Name,
            COALESCE(Measure1, Measure2) AS Measure,
            Ratio,
            PriceIn,
            ca.PriceOut AS PriceOut,
            MinQtty,
            NormalQtty,
            Description,
            Type,
            IsRecipe,
            TaxGroup,
            IsVeryUsed,
            GroupID,
            Deleted
        FROM dbo.Goods
        CROSS APPLY (
            SELECT TOP 1 PriceOut
            FROM (VALUES
                (PriceOut1),
                (PriceOut2),
                (PriceOut3),
                (PriceOut4),
                (PriceOut5),
                (PriceOut6),
                (PriceOut7),
                (PriceOut8),
                (PriceOut9),
                (PriceOut10)
            ) AS PriceTable(PriceOut)
            WHERE PriceOut > 0
            ORDER BY PriceOut
        ) ca
        WHERE 1 = 1
    """)

    if name:
        query = text(f"{query.text} AND Name LIKE :name")
    if code:
        query = text(f"{query.text} AND Code = :code")
    if barcode:
        query = text(f"{query.text} AND COALESCE(BarCode1, BarCode2, BarCode3) = :barcode")

    # Add Pagination
    query = text(f"{query.text} ORDER BY ID OFFSET :offset ROWS FETCH NEXT :page_size ROWS ONLY")

    result = mssql_db.execute(query, {
        "name": f"%{name}%" if name else None,
        "code": code,
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