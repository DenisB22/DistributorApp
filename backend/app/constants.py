class RoleName:
    ADMIN = "admin"
    STAFF = "staff"
    CLIENT = "client"


class OperationQueryParams:
    OPER_TYPE = "oper_type"
    OPER_NAME = "oper_name"
    GOOD_ID = "good_id"
    GOOD_NAME = "good_name"
    PARTNER_ID = "partner_id"
    PARTNER_NAME = "partner_name"

    @classmethod
    def values(cls):
        return [cls.OPER_TYPE, cls.OPER_NAME, cls.GOOD_ID, cls.GOOD_NAME, cls.PARTNER_ID, cls.PARTNER_NAME]
