from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.database import get_mssql_db

router = APIRouter(prefix="/microinvest", tags=["Microinvest"])


@router.get("/products")
def get_products(db: Session = Depends(get_mssql_db)):
    """Returns a list of products from Microinvest"""
    query = text("SELECT TOP 10 * FROM dbo.Goods")
    result = db.execute(query).mappings().all()  # Convert to dictionaries
    return {"products": result}