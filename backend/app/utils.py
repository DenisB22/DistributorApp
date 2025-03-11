from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import models
from app.db import database
from app.config import config

SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = config["ALGORITHM"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    scheme_name="JWT"
)


def get_password_hash(password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compares a hashed password with a plain text password."""
    return pwd_context.verify(plain_password, hashed_password)


def is_token_blacklisted(token: str, db: Session) -> bool:
    """Checks if the token is in the blacklist"""
    return db.query(models.TokenBlacklist).filter_by(token=token).first() is not None


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """Retrieves the currently authenticated user based on the provided token."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if is_token_blacklisted(token=token, db=db):
        raise HTTPException(
            status_code=401,
            detail="Token has been blacklisted. Please log in again."
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


