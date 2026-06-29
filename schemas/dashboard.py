from pydantic import BaseModel


class DepartmentStatistics(BaseModel):
    department_name: str
    employee_count: int


class AdminDashboardResponse(BaseModel):
    total_users: int
    total_employees: int
    total_departments: int

    average_age: float
    youngest_age: int
    oldest_age: int

    department_statistics: list[DepartmentStatistics]


class ManagerDashboardResponse(BaseModel):
    total_employees: int


class EmployeeDashboardResponse(BaseModel):
    full_name: str
    email: str
    department: str
