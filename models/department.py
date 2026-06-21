from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base
from models.base_audit import AuditMixin


class Department(Base, AuditMixin):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), unique=True, nullable=False)

    description = Column(String(255), nullable=True)

    employees = relationship(
        "Employee",
        back_populates="department",
        cascade="all, delete"
    )
