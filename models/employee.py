from sqlalchemy import Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from models.base_audit import AuditMixin
from core.database import Base


class Employee(Base, AuditMixin):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)

    # OLD COLUMN (keep for now)
    name = Column(String(50), nullable=False)

    # NEW COLUMNS
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)

    email = Column(String(100), nullable=False, unique=True)
    age = Column(Integer, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=True
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id")
    )

    department = relationship(
        "Department",
        back_populates="employees"
    )

    user = relationship(
        "User",
        back_populates="employee"
    )

    @hybrid_property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.name

    @full_name.expression
    def full_name(cls):
        return func.concat(
            cls.first_name,
            " ",
            cls.last_name
        )
