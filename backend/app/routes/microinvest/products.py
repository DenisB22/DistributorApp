from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import commons
from app.commons import is_superuser_based_on_user_level
from app.db.database import get_mssql_db
from app.models import UserMapping
from app.schemas.products import ProductResponse, ProductApiResponse
from app.utils import get_current_user_with_mapping

router = APIRouter(prefix="/microinvest/products", tags=["Microinvest - Products"])


@router.get("/", response_model=ProductApiResponse)
def get_products(
    mssql_db: Session = Depends(get_mssql_db),
    current_user_mapping: UserMapping = Depends(get_current_user_with_mapping),
    product_id: int = Query(None, description="Filter by product id"),
    name: str = Query(None, description="Filter by product name"),
    code: str = Query(None, description="Filter by code"),
    bar_code: str = Query(None, description="Filter by barcode"),
    # page: int = Query(1, ge=1, description="Page number (1-based index)"),
    limit: int = Query(20, le=100, description="Number of results per page (max 100)"),
    offset: int = Query(0, description="Offset for pagination", ge=0)
):
    """Returns a paginated list of products from Microinvest"""

    # offset = (page - 1) * limit  # Calculates where to start next page from
    print(f"NAME: {name}")
    print(f"CODE: {code}")
    print(f"BAR CODE: {bar_code}")

    query = text(f"""
        SELECT
            ID AS product_id,
            Code AS code,
            COALESCE(BarCode1, BarCode2, BarCode3) AS bar_code,
            COALESCE(Catalog1, Catalog2, Catalog3) AS catalog,
            COALESCE(Name, Name2) AS name,
            COALESCE(Measure1, Measure2) AS measure,
            Ratio AS ratio,
            PriceIn AS price_in,
            ca.price_out AS price_out,
            MinQtty AS min_qtty,
            NormalQtty AS normal_qtty,
            Description AS description,
            Type AS type,
            IsRecipe AS is_recipe,
            TaxGroup AS tax_group,
            IsVeryUsed AS is_very_used,
            GroupID AS group_id,
            Deleted AS deleted
        FROM dbo.Goods
        CROSS APPLY (
            SELECT TOP 1 price_out
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
            ) AS PriceTable(price_out)
            WHERE price_out > 0
            ORDER BY price_out
        ) ca
        WHERE 1 = 1
    """)

    if product_id:
        query = text(f"{query.text} AND ID = :product_id")
    if name:
        name = name.strip()
        query = text(f"{query.text} AND Name LIKE :name")
    if code:
        code = code.strip()
        query = text(f"{query.text} AND Code = :code")
    if bar_code:
        bar_code = bar_code.strip()
        query = text(f"{query.text} AND COALESCE(BarCode1, BarCode2, BarCode3) = :barcode")

    # Add Pagination
    query = text(f"{query.text} ORDER BY ID OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY")

    try:
        print(f"QUERY: {query}")
        products = mssql_db.execute(query, {
            "product_id": product_id,
            "name": f"%{name}%" if name else None,
            "code": code,
            "barcode": bar_code,
            "offset": offset,
            "limit": limit
        }).mappings().all()
        print(f"PRODUCTS: {products}")
        print(f"LIMIT: {limit}")
        print(f"OFFSET: {offset}")
        return {
            "offset": offset,
            "limit": limit,
            "total_records": len(products),
            "products": [
                ProductResponse(
                    product_id=row.product_id,
                    code=row.code,
                    bar_code=row.bar_code,
                    catalog=row.catalog,
                    name=row.name,
                    measure=row.measure,
                    ratio=row.ratio,
                    # Hide price_in for non-admins
                    price_in=row.price_in if is_superuser_based_on_user_level(current_user_mapping.user_level) else None,
                    price_out=row.price_out,
                    min_qtty=row.min_qtty,
                    normal_qtty=row.normal_qtty,
                    description=row.description,
                    type=row.type,
                    is_recipe=row.is_recipe,
                    tax_group=row.tax_group,
                    is_very_used=row.is_very_used,
                    group_id=row.group_id,
                    deleted=row.deleted,
                )
                for row in products
            ]
        }

    except Exception as e:
        return commons.return_http_400_response(f'An error occurred: {e}')