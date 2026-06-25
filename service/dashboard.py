from sqlalchemy.orm import Session

from models.user import User
from models.employee import Employee
from models.department import Department

from fastapi import HTTPException, status


class DashboardService:

    def __init__(self, db: Session):
        self.db = db

    def get_admin_dashboard(self):

        return {
            "total_users": self.db.query(User).count(),
            "total_employees": self.db.query(Employee).count(),
            "total_departments": self.db.query(Department).count(),
        }

    def get_manager_dashboard(self):

        return {
            "total_employees": self.db.query(Employee).count(),
        }

    def get_employee_dashboard(self, current_user):

        employee = current_user.employee

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee profile not found",
            )

        return {
            "full_name": employee.full_name,
            "email": employee.email,
            "department": employee.department.name,
        }