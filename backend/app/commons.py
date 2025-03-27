from fastapi import HTTPException
from app import models
from app.constants import RoleName
from app.enums.roles import MicroinvestUserLevel


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
    

def validate_start_date_before_end_date(start_date, end_date):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date!")
    return

def is_superuser_based_on_user_level(user_level):
    """Checks if the user is an admin or staff in Microinvest based on user level."""
    return user_level == MicroinvestUserLevel.SUPERUSER.value