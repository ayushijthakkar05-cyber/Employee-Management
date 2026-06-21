# core/enums.py

from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class OTPPurposeEnum(str, Enum):
    EMAIL_VERIFICATION = "email_verification"
    FORGOT_PASSWORD = "forgot_password"