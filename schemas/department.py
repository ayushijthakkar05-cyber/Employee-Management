from pydantic import BaseModel, Field, EmailStr
from uuid import UUID


# REQUEST SCHEMA
class DepartmentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: str | None = None


# BASIC DEPARTMENT
class DepartmentBasic(BaseModel):
    id: int
    uuid: UUID
    name: str

    class Config:
        from_attributes = True


# EMPLOYEE INSIDE DEPARTMENT
class DepartmentEmployeeResponse(BaseModel):
    id: int
    uuid: UUID

    name: str
    email: EmailStr
    age: int

    class Config:
        from_attributes = True


# FULL DEPARTMENT RESPONSE
class DepartmentResponse(BaseModel):
    id: int
    uuid: UUID

    name: str
    description: str | None = None

    class Config:
        from_attributes = True


# SINGLE DEPARTMENT WITH EMPLOYEES
class DepartmentDetailResponse(BaseModel):
    id: int
    uuid: UUID

    name: str
    description: str | None = None

    employees: list[DepartmentEmployeeResponse] = []

    class Config:
        from_attributes = True


# CREATE / UPDATE RESPONSE
class DepartmentCreateResponse(BaseModel):
    message: str
    department: DepartmentResponse


# LIST RESPONSE
class DepartmentListResponse(BaseModel):
    data: list[DepartmentResponse]


# JOIN RESPONSE
class DepartmentEmployeeJoinResponse(BaseModel):
    department_id: int
    department_uuid: UUID
    department_name: str

    employee_id: int | None = None
    employee_uuid: UUID | None = None

    employee_name: str | None = None
    employee_email: EmailStr | None = None


class DepartmentEmployeeJoinListResponse(BaseModel):
    data: list[DepartmentEmployeeJoinResponse]


# COMMON MESSAGE RESPONSE
class MessageResponse(BaseModel):
    message: str
