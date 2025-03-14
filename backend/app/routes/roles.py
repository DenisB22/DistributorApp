from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.schemas import role
from app.db import database
from app.utils import get_current_user
from app.constants import RoleName

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/roles/", response_model=role.Role)
def create_role(
    role: role.RoleCreate,
    db: Session = Depends(database.get_postgres_db),
    current_user: models.User = Depends(get_current_user)
):
    """Creates a new role (admins and superusers only)."""
    
    # Check if user has required rights
    if not (current_user.is_superuser or (current_user.role and current_user.role.name == RoleName.ADMIN)):
        raise HTTPException(status_code=403, detail="Only admins and superusers can create roles!")

    # Check if role already exists
    existing_role = db.query(models.Role).filter(models.Role.name == role.name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role already exists!")

    db_role = models.Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@router.get("/roles/", response_model=list[role.Role])
def get_roles(
    db: Session = Depends(database.get_postgres_db),
    current_user: models.User = Depends(get_current_user)
):
    """Returns all available roles (admins and superusers only)."""

    # Check if user has required rights
    if not (current_user.is_superuser or (current_user.role and current_user.role.name == RoleName.ADMIN)):
        raise HTTPException(status_code=403, detail="Only admins and superusers can view roles!")

    return db.query(models.Role).all()

