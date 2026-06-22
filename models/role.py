from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid as uuid_pkg
from core.database import Base


class Role(Base):

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        UUID(as_uuid=True),
        default=uuid_pkg.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="role")
