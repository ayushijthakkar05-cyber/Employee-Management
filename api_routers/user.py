from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db
from core.rbac import require_roles
from core.enums import RoleEnum

from service.user import UserService
from schemas.user import ManagerListResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/managers",
    response_model=ManagerListResponse,
)
def get_managers(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles([RoleEnum.ADMIN.value])),
):
    service = UserService(db)

    return service.get_managers()
