from fastapi import HTTPException
from app import models
from app.constants import RoleName


def return_http_400_response(message):
    raise HTTPException(status_code=400, detail=message)


def return_http_404_response(message):
    raise HTTPException(status_code=404, detail=message)


def return_http_403_response(message):
    raise HTTPException(status_code=403, detail=message)


def check_admin_or_staff(user: models.User):
    """Checks if the user is an admin or staff."""
    if not (user.is_superuser or user.role in [RoleName.ADMIN, RoleName.STAFF]):
        raise HTTPException(status_code=403, detail="You do not have permission!")