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

    def get_manager_dashboard(self, current_user):

        total_employees = (
            self.db.query(Employee)
            .filter(Employee.department_id == current_user.manager_department_id)
            .count()
        )

        return {
            "total_employees": total_employees,
        }

    def get_admin_dashboard(self):

        total_users = self.db.query(User).count()

        employees = self.db.query(Employee).all()

        total_employees = len(employees)

        total_departments = self.db.query(Department).count()

        if employees:

            ages = [employee.age for employee in employees]

            average_age = round(sum(ages) / len(ages), 2)

            youngest_age = min(ages)

            oldest_age = max(ages)

        else:

            average_age = 0

            youngest_age = 0

            oldest_age = 0

        department_statistics = []

        departments = self.db.query(Department).all()

        for department in departments:

            department_statistics.append(
                {
                    "department_name": department.name,
                    "employee_count": len(department.employees),
                }
            )

        return {
            "total_users": total_users,
            "total_employees": total_employees,
            "total_departments": total_departments,
            "average_age": average_age,
            "youngest_age": youngest_age,
            "oldest_age": oldest_age,
            "department_statistics": department_statistics,
        }
