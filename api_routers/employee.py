from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Literal

from schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeCreateResponse,
    EmployeeListResponse,
    EmployeeDepartmentJoinListResponse,
    EmployeeDepartmentLeftJoinListResponse,
    MessageResponse
)

from core.dependencies import get_db
from core.rbac import require_roles
from core.enums import RoleEnum

from service.employee import EmployeeService

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# Create employee (Admin only)
@router.post(
    "/",
    response_model=EmployeeCreateResponse
)
def create_emp(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles([RoleEnum.ADMIN.value])
    )
):

    service = EmployeeService(db)

    return service.create_employee(
        employee
    )


# List employees (Admin, Manager)
@router.get(
    "/",
    response_model=EmployeeListResponse
)
def read_employees(
    page: int = 1,
    limit: int = 5,
    search: str = None,
    age_from: int = None,
    age_to: int = None,

    sort: Literal[
        "id",
        "first_name",
        "last_name",
        "age",
        "full_name"
    ] = "id",

    order: Literal[
        "asc",
        "desc"
    ] = "asc",
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles([
            RoleEnum.ADMIN.value,
            RoleEnum.MANAGER.value
        ])
    )
):

    service = EmployeeService(db)

    return service.get_employees(
        page,
        limit,
        search,
        age_from,
        age_to,
        sort,
        order
    )


# Logged-in employee profile
@router.get(
    "/me",
    response_model=EmployeeResponse
)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles([RoleEnum.EMPLOYEE.value])
    )
):

    service = EmployeeService(db)

    return service.get_my_employee_profile(
        current_user
    )


# Update employee (Admin, Manager)
@router.put(
    "/{employee_id}",
    response_model=EmployeeCreateResponse
)
def update_emp(
    employee_id: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles([
            RoleEnum.ADMIN.value,
            RoleEnum.MANAGER.value
        ])
    )
):

    service = EmployeeService(db)

    return service.update_employee(
        employee_id,
        employee
    )


# Delete employee (Admin only)
@router.delete(
    "/{employee_id}",
    response_model=MessageResponse
)
def delete_emp(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles([RoleEnum.ADMIN.value])
    )
):

    service = EmployeeService(db)

    return service.delete_employee(
        employee_id
    )


# Employee + Department Inner Join (Admin, Manager)
@router.get(
    "/with-department",
    response_model=EmployeeDepartmentJoinListResponse
)
def read_employees_with_department(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles([
            RoleEnum.ADMIN.value,
            RoleEnum.MANAGER.value
        ])
    )
):

    service = EmployeeService(db)
    return service.get_employees_with_department()

#Employee+Department Left Join (Admin, Manager)
@router.get(
    "/left-join",
    response_model=EmployeeDepartmentLeftJoinListResponse
)
def read_employees_left_join(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles([
            RoleEnum.ADMIN.value,
            RoleEnum.MANAGER.value
        ])
    )
):

    service = EmployeeService(db)

    return service.get_employees_left_join()
