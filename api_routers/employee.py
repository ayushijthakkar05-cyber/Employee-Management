from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeCreateResponse,
    EmployeeListResponse,
    EmployeeDepartmentJoinListResponse,
    EmployeeDepartmentLeftJoinListResponse,
    MessageResponse,
    EmployeeStatisticsResponse,
)
from schemas.user import AssignManagerDepartmentRequest

from core.dependencies import get_db
from core.rbac import require_roles
from service.employee import EmployeeService
from service.auth import AuthService
from core.enums import RoleEnum, SortFieldEnum, SortOrderEnum

router = APIRouter(prefix="/employees", tags=["Employees"])


# Create employee (Admin only)
@router.post("/", response_model=EmployeeCreateResponse)
def create_emp(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([RoleEnum.ADMIN.value])),
):
    service = EmployeeService(db)

    return service.create_employee(employee)


# List employees (Admin, Manager)
@router.get("/", response_model=EmployeeListResponse)
def read_employees(
    page: int = 1,
    limit: int = 5,
    search: str = None,
    age_from: int = None,
    age_to: int = None,
    sort: SortFieldEnum = SortFieldEnum.id,
    order: SortOrderEnum = SortOrderEnum.asc,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.MANAGER.value])),
):
    service = EmployeeService(db)

    return service.get_employees(page, limit, search, age_from, age_to, sort, order,current_user,)



# Logged-in employee profile
@router.get("/me", response_model=EmployeeResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([RoleEnum.EMPLOYEE.value])),
):
    service = EmployeeService(db)

    return service.get_my_employee_profile(current_user)

# Employee + Department Inner Join (Admin, Manager)
@router.get("/with-department", response_model=EmployeeDepartmentJoinListResponse)
def read_employees_with_department(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.MANAGER.value])),
):
    service = EmployeeService(db)

    return service.get_employees_with_department()


# Employee + Department Left Join (Admin, Manager)
@router.get("/left-join", response_model=EmployeeDepartmentLeftJoinListResponse)
def read_employees_left_join(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.MANAGER.value])),
):
    service = EmployeeService(db)

    return service.get_employees_left_join()

@router.get(
    "/statistics",
    response_model=EmployeeStatisticsResponse,
)
def employee_statistics(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            [
                RoleEnum.ADMIN.value,
                RoleEnum.MANAGER.value,
            ]
        )
    ),
):
    service = EmployeeService(db)

    return service.get_employee_statistics(
    current_user
)

@router.get("/{employee_uuid}", response_model=EmployeeResponse)
def read_employee(
    employee_uuid: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            [
                RoleEnum.ADMIN.value,
                RoleEnum.MANAGER.value,
            ]
        )
    ),
):
    service = EmployeeService(db)

    return service.get_employee_by_uuid(
    employee_uuid,
    current_user,
)



# Update employee (Admin, Manager)
@router.put("/{employee_uuid}", response_model=EmployeeCreateResponse)
def update_emp(
    employee_uuid: UUID,
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.MANAGER.value])),
):
    service = EmployeeService(db)

    return service.update_employee(
    employee_uuid,
    employee,
    current_user,
)
@router.put(
    "/users/{user_uuid}/assign-department"
)
def assign_manager_department(
    user_uuid: UUID,
    request: AssignManagerDepartmentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            [RoleEnum.ADMIN.value]
        )
    ),
):
    service = AuthService(db)

    return service.assign_manager_department(
        user_uuid,
        request.department_id,
    )

# Delete employee (Admin only)
@router.delete("/{employee_uuid}", response_model=MessageResponse)
def delete_emp(
    employee_uuid: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([RoleEnum.ADMIN.value])),
):
    service = EmployeeService(db)

    return service.delete_employee(
    employee_uuid,
    current_user,
)


