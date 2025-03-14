from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, commons
from app.schemas import user
from app.db import database
from app.utils import get_password_hash, get_current_user
from app.constants import RoleName

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=user.User)
def create_user(
    user: user.UserCreate,
    db: Session = Depends(database.get_postgres_db),
    current_user: models.User = Depends(get_current_user),  # Get the current user
):
    """Only superusers can create new users."""

    # Only superusers and staff are allowed to create new users
    if not (current_user.is_superuser or current_user.role.name == RoleName.ADMIN):
        message = "You do not have permission to create users."
        return commons.return_http_400_response(message)

    # Check if the email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        message = "User with this email already exists."
        return commons.return_http_400_response(message)

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create a new user
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
        is_superuser=user.is_superuser,  # Can be set only by a superuser
        is_active=True,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=Union[List[user.User], None])
def get_all_users(
    db: Session = Depends(database.get_postgres_db),
    current_user: models.User = Depends(get_current_user)
):
    """Only superusers and staff can retrieve the list of all users."""

    if not (current_user.is_superuser or current_user.role.name == RoleName.ADMIN):
        message = "Only superusers can retrieve list of all users!"
        return commons.return_http_403_response(message)
    
    users = db.query(models.User).all()
    return users


@router.get("/{user_id}", response_model=Union[user.User, None])
def get_user(
    user_id: int,
    db: Session = Depends(database.get_postgres_db),
    current_user: models.User = Depends(get_current_user)
):  
    """Only superusers and staff can retrieve a specific user."""

    if not (current_user.is_superuser or current_user.role.name == RoleName.ADMIN) and current_user.id != user_id:
        message = "You do not have permission to retrieve this user!"
        return commons.return_http_403_response(message)
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        message = "User not found!"
        return commons.return_http_404_response(message)
    return user 


@router.put("/{user_id}", response_model=Union[user.User, None])
def update_user(
    user_id: int,
    user_to_update: user.UserUpdate,
    db: Session = Depends(database.get_postgres_db),
    current_user: models.User = Depends(get_current_user)
):
    """Allows updating user details (only superuser, staff or the user themselves)."""

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return commons.return_http_404_response("User not found!")

    # Only superuser, staff or the user themselves can update the profile
    if not (current_user.is_superuser or current_user.role.name == RoleName.ADMIN) and current_user.id != user.id:
        return commons.return_http_403_response("You do not have permission to edit this user!")

    # Validate unique username
    if user_to_update.username and user_to_update.username != user.username:
        if db.query(models.User).filter(models.User.username == user_to_update.username).first():
            return commons.return_http_400_response("Username is already taken!")

    # Validate unique email
    if user_to_update.email and user_to_update.email != user.email:
        if db.query(models.User).filter(models.User.email == user_to_update.email).first():
            return commons.return_http_400_response("Email is already taken!")

    # Ensure only superusers and staff can modify certain fields
    if (user_to_update.is_superuser is not None or user_to_update.is_active is not None) and not (current_user.is_superuser or current_user.role.name == RoleName.ADMIN):
        return commons.return_http_403_response("You do not have permission to edit these fields!")

    # Update allowed fields
    update_fields = ["first_name", "last_name", "email", "username"]
    for field in update_fields:
        value = getattr(user_to_update, field, None)
        if value:
            setattr(user, field, value)

    # Update password if provided
    if user_to_update.password:
        user.hashed_password = get_password_hash(user_to_update.password)

    # Only superusers and staff can modify is_superuser and is_active
    if (current_user.is_superuser or current_user.role.name == RoleName.ADMIN):

        user.is_superuser = user_to_update.is_superuser if user_to_update.is_superuser is not None else user.is_superuser
        user.is_active = user_to_update.is_active if user_to_update.is_active is not None else user.is_active

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int, 
    db: Session = Depends(database.get_postgres_db), 
    current_user: models.User = Depends(get_current_user)
):
    """Only superusers and staff can delete users."""
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if not (current_user.is_superuser or current_user.role.name == RoleName.ADMIN):
        raise HTTPException(status_code=403, detail="You do not have permission to delete users.")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully."}

