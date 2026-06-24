from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"


class OTPPurposeEnum(str, Enum):
    EMAIL_VERIFICATION = "email_verification"
    FORGOT_PASSWORD = "forgot_password"


class SortFieldEnum(str, Enum):
    id = "id"
    first_name = "first_name"
    last_name = "last_name"
    email = "email"
    age = "age"


class SortOrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"
