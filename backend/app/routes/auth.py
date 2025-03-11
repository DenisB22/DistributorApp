from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app import models, utils
from app.schemas import token, user
from app.db import database
from app.utils import get_current_user, oauth2_scheme
from app.config import config

SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = config["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = config["ACCESS_TOKEN_EXPIRE_MINUTES"]

router = APIRouter(prefix="/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def common_login(user, password):
    if not user or not utils.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is deactivated")

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/json", response_model=token.Token)
def login_json(request: user.LoginRequest, db: Session = Depends(database.get_db)):
    """Login with JSON (For Postman, Mobile Apps, etc.)"""
    user = db.query(models.User).filter(models.User.email == request.email).first()

    return common_login(user, request.password)


@router.post("/login", response_model=token.Token)
def login_oauth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    """Login with OAuth2 Password Flow (Swagger UI)"""

    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    return common_login(user, form_data.password)


@router.get("/me", response_model=user.User)
def get_current_user(
        current_user: models.User = Depends(get_current_user)
):
    """Returns information about the currently logged-in user."""
    return current_user


@router.post("/logout")
def logout(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)
):
    """Adds token to the blacklist upon logout"""

    existing_token = db.query(models.TokenBlacklist).filter_by(token=token).first()
    
    if existing_token:
        return {"message": "Token is already blacklisted"}
    
    db_token = models.TokenBlacklist(token=token)
    db.add(db_token)
    db.commit()
    return {"message": "Successfully logged out"}
