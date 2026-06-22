from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid as uuid_pkg
from core.database import Base


class UserOTP(Base):

    __tablename__ = "user_otps"

    id = Column(Integer, primary_key=True, index=True)

    uuid = Column(
        UUID(as_uuid=True),
        default=uuid_pkg.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    otp = Column(String, nullable=False)

    purpose = Column(String, nullable=False)

    expires_at = Column(DateTime, nullable=False)

    is_used = Column(Boolean, default=False)

    user = relationship("User", back_populates="otps")
