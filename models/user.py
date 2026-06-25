from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base
from models.base_audit import AuditMixin
from sqlalchemy.dialects.postgresql import UUID
import uuid as uuid_pkg


class User(Base, AuditMixin):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        UUID(as_uuid=True),
        default=uuid_pkg.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )

    username = Column(String, unique=True, nullable=False, index=True)

    email = Column(String, unique=True, nullable=False, index=True)

    password_hash = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users")

    is_active = Column(Boolean, default=True)

    is_verified = Column(Boolean, default=False)

    manager_department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=True
    )
    otps = relationship("UserOTP", back_populates="user")

    # One User -> One Employee
    employee = relationship("Employee", back_populates="user", uselist=False)
    
    manager_department = relationship("Department")
