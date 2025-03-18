from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.db.database import get_postgres_db, get_mssql_db
from app.models import User, UserMapping
from app.schemas.user_mapping import UserMappingCreate, UserMappingResponse
from app.utils import get_current_user
from app.constants import RoleName

router = APIRouter(prefix="/microinvest/users", tags=["Microinvest - Users"])

@router.post("/map", response_model=UserMappingResponse)
def map_user(
    mapping_data: UserMappingCreate,
    db: Session = Depends(get_postgres_db),
    mssql_db: Session = Depends(get_mssql_db),
    current_user: User = Depends(get_current_user)
):
    """Links an existing user to a Microinvest user (Admin/Superuser only)."""

    # Only superusers or admins can perform user mapping
    if not (current_user.is_superuser or current_user.role.name == RoleName.ADMIN):
        raise HTTPException(status_code=403, detail="You do not have permission to map users.")
    

     # Validate that the user exists in PostgreSQL
    user = db.query(User).filter(User.id == mapping_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found in PostgreSQL database.")
    
    # Validate that the Microinvest user exists in the Microinvest database
    microinvest_user = mssql_db.execute(
        text("SELECT ID, UserLevel FROM dbo.Users WHERE ID = :user_id"),
        {"user_id": mapping_data.microinvest_user_id}
    ).fetchone()

    if not microinvest_user:
        raise HTTPException(status_code=404, detail="User not found in Microinvest database.")
    
    # Check if the user is already mapped
    existing_mapping = db.query(UserMapping).filter(UserMapping.user_id == current_user.id).first()
    if existing_mapping:
        raise HTTPException(status_code=400, detail="User is already mapped to a Microinvest user.")

    # Ensure the Microinvest user ID is not already assigned to another user
    existing_microinvest_user = db.query(UserMapping).filter(UserMapping.microinvest_user_id == mapping_data.microinvest_user_id).first()
    if existing_microinvest_user:
        raise HTTPException(status_code=400, detail="This Microinvest user is already mapped to another account.")
    
    user_level = microinvest_user.UserLevel

    # Create a new mapping entry
    new_mapping = UserMapping(
        user_id=current_user.id,
        microinvest_user_id=mapping_data.microinvest_user_id,
        user_level=user_level
    )

    db.add(new_mapping)
    db.commit()
    db.refresh(new_mapping)

    # return {"message": "User successfully mapped!", "user_id": current_user.id, "microinvest_user_id": mapping_data.microinvest_user_id}
    return new_mapping


@router.delete("/{user_id}", status_code=200)
def unmap_user(
    user_id: int,
    db: Session = Depends(get_postgres_db),
    current_user: User = Depends(get_current_user)
):
    """Removes a mapping between a PostgreSQL user and a Microinvest user (Admin/Superuser only)"""

    # Only superusers or admins can perform user mapping
    if not (current_user.is_superuser or current_user.role.name == RoleName.ADMIN):
        raise HTTPException(status_code=403, detail="You do not have permission to unmap users.")
    
    # Validate that the user exists in PostgreSQL
    mapping = db.query(UserMapping).filter(UserMapping.id == user_id).first()
    if not mapping:
        raise HTTPException(status_code=404, detail="User mapping not found.")
    
    # Delete mapping
    db.delete(mapping)
    db.commit()

    return {"messasge": "User successfully unmapped."}
    



