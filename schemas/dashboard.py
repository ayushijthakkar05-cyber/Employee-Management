from pydantic import BaseModel


class AdminDashboardResponse(BaseModel):
    total_users: int
    total_employees: int
    total_departments: int


class ManagerDashboardResponse(BaseModel):
    total_employees: int


class EmployeeDashboardResponse(BaseModel):
    full_name: str
    email: str
    department: str