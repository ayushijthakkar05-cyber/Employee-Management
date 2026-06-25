from pydantic import BaseModel


class AssignManagerDepartmentRequest(BaseModel):
    department_id: int
    