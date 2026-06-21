from core.decorators import simple_log
from sqlalchemy.orm import Session
from models.employee import Employee
from models.department import Department
from models.user import User
from fastapi import HTTPException, status


class EmployeeService:

    def __init__(self, db: Session):
        self.db = db

    @simple_log
    def create_employee(self, employee):

        existing = self.db.query(Employee).filter(
            Employee.email == employee.email
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        department = self.db.query(Department).filter(
            Department.id == employee.department_id
        ).first()

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        new_employee = Employee(
            name=f"{employee.first_name} {employee.last_name}",
            first_name=employee.first_name,
            last_name=employee.last_name,
            email=employee.email,
            age=employee.age,
            department_id=employee.department_id
        )

        user = self.db.query(User).filter(
            User.email == employee.email
        ).first()

        if user:
            new_employee.user_id = user.id

        self.db.add(new_employee)
        self.db.commit()
        self.db.refresh(new_employee)

        return {
            "message": "Employee created successfully",
            "employee": new_employee
        }

    @simple_log
    def get_employees(
        self,
        page,
        limit,
        search,
        age_from,
        age_to,
        sort,
        order
    ):

        skip = (page - 1) * limit

        query = self.db.query(Employee)

        if search:
            if search.isdigit():
                query = query.filter(
                    Employee.age == int(search)
                )
            else:
                query = query.filter(
                    Employee.full_name.ilike(f"%{search}%")
                )

        if age_from is not None:
            query = query.filter(
                Employee.age >= age_from
            )

        if age_to is not None:
            query = query.filter(
                Employee.age <= age_to
            )

        allowed_sort = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "age"
        ]

        if sort not in allowed_sort:
            sort = "id"

        sort_column = getattr(Employee, sort)

        if order == "desc":
            query = query.order_by(
                sort_column.desc()
            )
        else:
            query = query.order_by(
                sort_column.asc()
            )

        total = query.count()

        employees = query.offset(skip).limit(limit).all()

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "search": search,
            "age_from": age_from,
            "age_to": age_to,
            "sort": sort,
            "order": order,
            "data": employees
        }

    @simple_log
    def update_employee(
        self,
        employee_id,
        employee
    ):

        db_employee = self.db.query(Employee).filter(
            Employee.id == employee_id
        ).first()

        if not db_employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        department = self.db.query(Department).filter(
            Department.id == employee.department_id
        ).first()

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        existing = self.db.query(Employee).filter(
            Employee.email == employee.email,
            Employee.id != employee_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        db_employee.name = (
            f"{employee.first_name} {employee.last_name}"
        )

        db_employee.first_name = employee.first_name
        db_employee.last_name = employee.last_name
        db_employee.email = employee.email
        db_employee.age = employee.age
        db_employee.department_id = employee.department_id

        self.db.commit()
        self.db.refresh(db_employee)

        return {
            "message": "Employee updated successfully",
            "employee": db_employee
        }

    @simple_log
    def delete_employee(self, employee_id):

        db_employee = self.db.query(Employee).filter(
            Employee.id == employee_id
        ).first()

        if not db_employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        self.db.delete(db_employee)
        self.db.commit()

        return {
            "message": "Employee deleted successfully"
        }

    @simple_log
    def get_employees_with_department(self):

        results = (
            self.db.query(Employee, Department)
            .join(
                Department,
                Employee.department_id == Department.id
            )
            .all()
        )

        return {
            "data": [
                {
                    "employee_id": emp.id,
                    "first_name": emp.first_name,
                    "last_name": emp.last_name,
                    "full_name": emp.full_name,
                    "email": emp.email,
                    "department_id": dept.id,
                    "department_name": dept.name
                }
                for emp, dept in results
            ]
        }

    @simple_log
    def get_employees_left_join(self):

        results = (
            self.db.query(Employee, Department)
            .outerjoin(
                Department,
                Employee.department_id == Department.id
            )
            .all()
        )

        return {
            "data": [
                {
                    "employee_id": emp.id,
                    "first_name": emp.first_name,
                    "last_name": emp.last_name,
                    "full_name": emp.full_name,
                    "department_id": dept.id if dept else None,
                    "department_name": dept.name if dept else None
                }
                for emp, dept in results
            ]
        }

    @simple_log
    def get_my_employee_profile(self, current_user):

        if not current_user.employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee profile not linked to this user"
            )

        return current_user.employee
