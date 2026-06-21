from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
    ConfigDict
)


def validate_password_strength(value: str) -> str:

    if not any(c.isupper() for c in value):
        raise ValueError(
            "Password must contain an uppercase letter"
        )

    if not any(c.isdigit() for c in value):
        raise ValueError(
            "Password must contain a number"
        )

    return value


class UserCreate(BaseModel):

    # Allows both alias and original field names
    model_config = ConfigDict(
        populate_by_name=True
    )

    username: str = Field(
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        min_length=8
    )

    # Frontend can send confirmPassword
    confirm_password: str = Field(
        alias="confirmPassword"
    )

    # Frontend can send roleId
    role_id: int = Field(
        alias="roleId"
    )

    @model_validator(mode="before")
    @classmethod
    def normalize_email(cls, data: dict) -> dict:

        if "email" in data:
            data["email"] = data["email"].lower()

        return data

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)

    @model_validator(mode="after")
    def passwords_match(self):

        if self.password != self.confirm_password:
            raise ValueError(
                "Passwords do not match"
            )

        return self


class LoginRequest(BaseModel):

    email: EmailStr
    password: str


class ChangePasswordRequest(BaseModel):

    # Allows both alias and original field names
    model_config = ConfigDict(
        populate_by_name=True
    )

    # Frontend can send oldPassword
    old_password: str = Field(
        alias="oldPassword"
    )

    # Frontend can send newPassword
    new_password: str = Field(
        alias="newPassword",
        min_length=8
    )

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value: str) -> str:
        return validate_password_strength(value)


class RoleResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleResponse
    is_active: bool

    class Config:
        from_attributes = True


class RegisterResponse(BaseModel):
    message: str
    user: UserResponse


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


# Success message response
class MessageResponse(BaseModel):
    message: str


# Success message response for manager/admin/employee dashboard
class DashboardResponse(BaseModel):
    message: str
    user: str
