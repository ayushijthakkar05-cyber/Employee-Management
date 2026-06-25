from core.decorators import simple_log
from sqlalchemy.orm import Session
from models.employee import Employee
from models.department import Department
from models.user import User
from fastapi import HTTPException, status
from typing import Literal
from core.enums import SortFieldEnum, SortOrderEnum
from uuid import UUID
from sqlalchemy import func

class EmployeeService:

    def __init__(self, db: Session):
        self.db = db

    @simple_log
    def create_employee(self, employee):

        existing = (
            self.db.query(Employee).filter(Employee.email == employee.email).first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

        department = (
            self.db.query(Department)
            .filter(Department.id == employee.department_id)
            .first()
        )

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
            )

        new_employee = Employee(
            name=f"{employee.first_name} {employee.last_name}",
            first_name=employee.first_name,
            last_name=employee.last_name,
            email=employee.email,
            age=employee.age,
            department_id=employee.department_id,
        )

        user = self.db.query(User).filter(User.email == employee.email).first()

        if user:
            new_employee.user_id = user.id

        self.db.add(new_employee)
        self.db.commit()
        self.db.refresh(new_employee)

        return {"message": "Employee created successfully", "employee": new_employee}

    @simple_log
    def get_employees(
        self,
        page,
        limit,
        search,
        age_from,
        age_to,
        sort: SortFieldEnum = SortFieldEnum.id,
        order: SortOrderEnum = SortOrderEnum.asc,
        current_user=None,
    ):

        sort = sort.value
        order = order.value

        skip = (page - 1) * limit

        query = self.db.query(Employee)
        if current_user.role.name == "MANAGER":
             query = query.filter(
            Employee.department_id == current_user.manager_department_id
    )
        if (
            current_user
            and current_user.role.name == "manager"
    ):
            query = query.filter(
            Employee.department_id
            == current_user.manager_department_id
        )

        if search:
            if search.isdigit():
                query = query.filter(Employee.age == int(search))
            else:
                query = query.filter(Employee.full_name.ilike(f"%{search}%"))

        if age_from is not None:
            query = query.filter(Employee.age >= age_from)

        if age_to is not None:
            query = query.filter(Employee.age <= age_to)

        allowed_sort = {
            "id": Employee.id,
            "first_name": Employee.first_name,
            "last_name": Employee.last_name,
            "full_name": Employee.full_name,
            "email": Employee.email,
            "age": Employee.age,
        }

        sort_column = allowed_sort[sort]

        if order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        total = query.count()

        employees = query.offset(skip).limit(limit).all()

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "search": search,
            "age_from": age_from,
            "age_to": age_to,
            "sort": sort,
            "order": order,
            "data": employees,
            
        }

    @simple_log
    def update_employee(self, employee_uuid: UUID, employee):
        db_employee = (
            self.db.query(Employee).filter(Employee.uuid == employee_uuid).first()
        )
        if not db_employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
            )

        department = (
            self.db.query(Department)
            .filter(Department.id == employee.department_id)
            .first()
        )

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
            )

        existing = (
            self.db.query(Employee)
            .filter(Employee.email == employee.email, Employee.uuid != employee_uuid)
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

        db_employee.name = f"{employee.first_name} {employee.last_name}"

        db_employee.first_name = employee.first_name
        db_employee.last_name = employee.last_name
        db_employee.email = employee.email
        db_employee.age = employee.age
        db_employee.department_id = employee.department_id

        self.db.commit()
        self.db.refresh(db_employee)

        return {"message": "Employee updated successfully", "employee": db_employee}

    @simple_log
    def delete_employee(self, employee_uuid: UUID):

        db_employee = (
            self.db.query(Employee).filter(Employee.uuid == employee_uuid).first()
        )

        if not db_employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
            )

        self.db.delete(db_employee)
        self.db.commit()

        return {"message": "Employee deleted successfully"}

    @simple_log
    def get_employees_with_department(self):

        results = (
            self.db.query(Employee, Department)
            .join(Department, Employee.department_id == Department.id)
            .all()
        )

        return {
            "data": [
                {
                    "employee_id": emp.id,
                    "employee_uuid": emp.uuid,
                    "first_name": emp.first_name,
                    "last_name": emp.last_name,
                    "full_name": emp.full_name,
                    "email": emp.email,
                    "department_id": dept.id,
                    "department_uuid": dept.uuid,
                    "department_name": dept.name,
                }
                for emp, dept in results
            ]
        }

    @simple_log
    def get_employees_left_join(self):

        results = (
            self.db.query(Employee, Department)
            .outerjoin(Department, Employee.department_id == Department.id)
            .all()
        )

        return {
            "data": [
                {
                    "employee_id": emp.id,
                    "employee_uuid": emp.uuid,
                    "first_name": emp.first_name,
                    "last_name": emp.last_name,
                    "full_name": emp.full_name,
                    "department_id": dept.id if dept else None,
                    "department_uuid": dept.uuid if dept else None,
                    "department_name": dept.name if dept else None,
                }
                for emp, dept in results
            ]
        }
    @simple_log
    def get_employee_by_uuid(self, employee_uuid: UUID):

        employee = (
            self.db.query(Employee)
            .filter(Employee.uuid == employee_uuid)
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        return employee
    
    @simple_log
    def get_employee_statistics(self):

        total = self.db.query(Employee).count()

        average_age = (
            self.db.query(func.avg(Employee.age))
            .scalar()
        )

        youngest_age = (
            self.db.query(func.min(Employee.age))
            .scalar()
        )

        oldest_age = (
            self.db.query(func.max(Employee.age))
            .scalar()
        )

        return {
            "total_employees": total,
            "average_age": round(average_age or 0, 2),
            "youngest_age": youngest_age or 0,
            "oldest_age": oldest_age or 0,
        }
        
        
    @simple_log
    def get_my_employee_profile(self, current_user):

        employee = (
            self.db.query(Employee)
            .filter(Employee.user_id == current_user.id)
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee profile not found"
            )

        return employee    