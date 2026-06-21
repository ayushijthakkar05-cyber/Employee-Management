from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from schemas.department import DepartmentBasic


# REQUEST SCHEMA
class EmployeeCreate(BaseModel):

    # Allows both alias and original field names
    model_config = ConfigDict(
        populate_by_name=True
    )

    # Frontend can send firstName
    first_name: str = Field(
        ...,
        alias="firstName",
        min_length=2,
        max_length=50
    )

    # Frontend can send lastName
    last_name: str = Field(
        ...,
        alias="lastName",
        min_length=2,
        max_length=50
    )

    email: EmailStr

    age: int = Field(
        ...,
        ge=18,
        le=60
    )

    # Frontend can send departmentId
    department_id: int = Field(
        alias="departmentId"
    )

    @field_validator("first_name", "last_name")
    @classmethod
    def name_must_be_alpha(cls, v):
        if any(char.isdigit() for char in v):
            raise ValueError(
                "Name cannot contain numbers"
            )
        return v


# RESPONSE SCHEMA
class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    full_name: str
    email: EmailStr
    age: int
    department: DepartmentBasic

    class Config:
        from_attributes = True


# CREATE / UPDATE RESPONSE
class EmployeeCreateResponse(BaseModel):
    message: str
    employee: EmployeeResponse


# LIST RESPONSE
class EmployeeListResponse(BaseModel):
    page: int
    limit: int
    total: int

    search: str | None = None
    age_from: int | None = None
    age_to: int | None = None

    sort: str
    order: str

    data: list[EmployeeResponse]


# INNER JOIN RESPONSE
class EmployeeDepartmentJoinResponse(BaseModel):
    employee_id: int
    first_name: str
    last_name: str
    full_name: str
    email: EmailStr

    department_id: int
    department_name: str


class EmployeeDepartmentJoinListResponse(BaseModel):
    data: list[EmployeeDepartmentJoinResponse]


# LEFT JOIN RESPONSE
class EmployeeDepartmentLeftJoinResponse(BaseModel):
    employee_id: int
    first_name: str
    last_name: str
    full_name: str

    department_id: int | None = None
    department_name: str | None = None


class EmployeeDepartmentLeftJoinListResponse(BaseModel):
    data: list[EmployeeDepartmentLeftJoinResponse]


# COMMON MESSAGE RESPONSE
class MessageResponse(BaseModel):
    message: str