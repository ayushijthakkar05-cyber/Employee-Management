from sqlalchemy.orm import Session
from models.department import Department
from models.employee import Employee
from fastapi import HTTPException, status
from core.decorators import simple_log
from uuid import UUID
from sqlalchemy import func


class DepartmentService:

    def __init__(self, db: Session):
        self.db = db

    # CREATE
    @simple_log
    def create_department(self, department):

        existing = (
            self.db.query(Department).filter(Department.name == department.name).first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department already exists",
            )

        dept = Department(
            name=department.name,
            description=department.description,
        )

        self.db.add(dept)
        self.db.commit()
        self.db.refresh(dept)

        return {"message": "Department created successfully", "department": dept}

    # READ
    @simple_log
    def get_departments(self):

        departments = self.db.query(Department).all()

        return {"data": departments}

    # UPDATE
    @simple_log
    def update_department(self, department_uuid: UUID, department):

        db_department = (
            self.db.query(Department).filter(Department.uuid == department_uuid).first()
        )

        if not db_department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
            )

        existing = (
            self.db.query(Department)
            .filter(
                Department.name == department.name, Department.uuid != department_uuid
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department already exists",
            )

        db_department.name = department.name
        db_department.description = department.description

        self.db.commit()
        self.db.refresh(db_department)

        return {
            "message": "Department updated successfully",
            "department": db_department,
        }

    @simple_log
    def delete_department(self, department_uuid: UUID):

        db_department = (
            self.db.query(Department)
            .filter(Department.uuid == department_uuid)
            .first()
        )

        if not db_department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        employee_count = (
            self.db.query(Employee)
            .filter(
                Employee.department_id == db_department.id
            )
            .count()
        )

        if employee_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete department with employees"
            )

        self.db.delete(db_department)
        self.db.commit()

        return {
            "message": "Department deleted successfully"
        }
    # GET SINGLE DEPARTMENT WITH EMPLOYEES
    @simple_log
    def get_department_by_id(self, department_uuid: UUID):

        department = (
            self.db.query(Department).filter(Department.uuid == department_uuid).first()
        )

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
            )

        return department

    # RIGHT JOIN CONCEPT
    @simple_log
    def get_departments_with_employees(self):

        results = (
            self.db.query(Department, Employee)
            .outerjoin(Employee, Employee.department_id == Department.id)
            .all()
        )

        return {
            "data": [
                {
                    "department_id": dept.id,
                    "department_uuid": dept.uuid,
                    "department_name": dept.name,
                    "employee_id": emp.id if emp else None,
                    "employee_uuid": emp.uuid if emp else None,
                    "employee_name": emp.name if emp else None,
                    "employee_email": emp.email if emp else None,
                }
                for dept, emp in results
            ]
        }
    @simple_log
    def get_department_statistics(
        self,
        current_user=None,
    ):

        query = (
            self.db.query(
                Department.name,
                func.count(Employee.id)
            )
            .outerjoin(
                Employee,
                Employee.department_id == Department.id
            )
        )

        if current_user.role.name == "MANAGER":
            query = query.filter(
                Department.id
                == current_user.manager_department_id
            )

        results = (
            query
            .group_by(Department.name)
            .all()
        )

        return {
            "data": [
                {
                    "department_name": name,
                    "employee_count": count,
                }
                for name, count in results
            ]
        }
        
    @simple_log
    def get_department_employees(
    self,
    department_uuid: UUID,
    current_user=None,
):

        department = (
            self.db.query(Department)
            .filter(
                Department.uuid == department_uuid
            )
            .first()
        )

        if not department:
            raise HTTPException(
                status_code=404,
                detail="Department not found",
            )
            
        if (
            current_user.role.name == "MANAGER"
            and department.id
            != current_user.manager_department_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

        return {
            "department_name": department.name,
            "employees": department.employees,
        }    
        
        