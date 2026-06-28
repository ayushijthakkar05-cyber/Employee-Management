from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db
from core.rbac import require_roles
from core.enums import RoleEnum

from service.dashboard import DashboardService

from schemas.dashboard import (
    AdminDashboardResponse,
    ManagerDashboardResponse,
    EmployeeDashboardResponse,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

@router.get(
    "/admin",
    response_model=AdminDashboardResponse,
)
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles([RoleEnum.ADMIN.value])
    ),
):
    service = DashboardService(db)

    return service.get_admin_dashboard()

@router.get(
    "/manager",
    response_model=ManagerDashboardResponse,
)
def manager_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles([RoleEnum.MANAGER.value])
    ),
):
    service = DashboardService(db)

    return service.get_manager_dashboard(current_user)

@router.get(
    "/employee",
    response_model=EmployeeDashboardResponse,
)
def employee_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles([RoleEnum.EMPLOYEE.value])
    ),
):
    service = DashboardService(db)

    return service.get_employee_dashboard(current_user)

