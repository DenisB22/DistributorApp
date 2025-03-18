from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    role_id = Column(Integer, ForeignKey("roles.id")) # FK to roles
    role = relationship("Role", back_populates="users")
    # mapping with `UserMapping`
    mapping = relationship("UserMapping", back_populates="user", uselist=False)


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False) # 'admin', 'staff', 'client', etc.

    users = relationship("User", back_populates="role")


class UserMapping(Base):
    __tablename__ = "user_mapping"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    microinvest_user_id = Column(Integer, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    user_level = Column(Integer, nullable=False)  # New field to store UserLevel

    # Relationship for easy access
    user = relationship("User", back_populates="mapping")




