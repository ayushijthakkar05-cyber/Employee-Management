from uuid import UUID

from pydantic import BaseModel


class AssignManagerDepartmentRequest(BaseModel):
    department_id: int


class ManagerResponse(BaseModel):
    uuid: UUID
    username: str
    email: str
    manager_department_id: int | None = None

    model_config = {
        "from_attributes": True
    }


class ManagerListResponse(BaseModel):
    data: list[ManagerResponse]