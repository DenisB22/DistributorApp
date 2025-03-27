from enum import Enum
from app.db.database import PostgresSessionLocal
from app import models


def get_roles():
    role_lst = []
    db = PostgresSessionLocal()
    role_model = db.query(models.Role).all()
    for item in role_model:
        role_lst.append(item.name)
    db.close()
    return role_lst


EnumRoles = Enum("Role", {name: name for name in get_roles()}, type=str)


class MicroinvestUserLevel(Enum):
    NORMAL_USER = 0  # Standard user without admin privileges
    SUPERUSER = 3  # Admin-level access in Microinvest