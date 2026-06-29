from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db
from core.rbac import require_roles
from core.enums import RoleEnum

from schemas.department import (
    DepartmentCreate,
    DepartmentCreateResponse,
    DepartmentListResponse,
    DepartmentDetailResponse,
    DepartmentEmployeeJoinListResponse,
    MessageResponse,
    DepartmentStatisticsListResponse,
    DepartmentEmployeesResponse,
)

from service.department import DepartmentService

router = APIRouter(prefix="/departments", tags=["Departments"])


# Create Department (Admin only)
@router.post("/", response_model=DepartmentCreateResponse)
def create_dept(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([RoleEnum.ADMIN.value])),
):
    service = DepartmentService(db)

    return service.create_department(department)


# Get All Departments
@router.get("/", response_model=DepartmentListResponse)
def read_departments(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            [RoleEnum.ADMIN.value, RoleEnum.MANAGER.value, RoleEnum.EMPLOYEE.value]
        )
    ),
):
    service = DepartmentService(db)

    return service.get_departments()


# Department + Employees Join
@router.get("/with-employees", response_model=DepartmentEmployeeJoinListResponse)
def read_departments_with_employees(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([RoleEnum.ADMIN.value, RoleEnum.MANAGER.value])),
):
    service = DepartmentService(db)

    return service.get_departments_with_employees()


@router.get(
    "/statistics",
    response_model=DepartmentStatisticsListResponse,
)
def department_statistics(
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
    service = DepartmentService(db)

    return service.get_department_statistics(current_user)


@router.get(
    "/{department_uuid}/employees",
    response_model=DepartmentEmployeesResponse,
)
def read_department_employees(
    department_uuid: UUID,
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
    service = DepartmentService(db)

    return service.get_department_employees(
        department_uuid,
        current_user,
    )


# Get Single Department
@router.get("/{department_uuid}", response_model=DepartmentDetailResponse)
def read_department(
    department_uuid: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            [RoleEnum.ADMIN.value, RoleEnum.MANAGER.value, RoleEnum.EMPLOYEE.value]
        )
    ),
):
    service = DepartmentService(db)

    return service.get_department_by_id(department_uuid)


# Update Department
@router.put("/{department_uuid}", response_model=DepartmentCreateResponse)
def update_dept(
    department_uuid: UUID,
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([RoleEnum.ADMIN.value])),
):
    service = DepartmentService(db)

    return service.update_department(department_uuid, department)


# Delete Department
@router.delete("/{department_uuid}", response_model=MessageResponse)
def delete_dept(
    department_uuid: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([RoleEnum.ADMIN.value])),
):
    service = DepartmentService(db)

    return service.delete_department(department_uuid)
