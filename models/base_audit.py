from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func


class AuditMixin:

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    created_by = Column(
        Integer,
        nullable=True
    )

    updated_by = Column(
        Integer,
        nullable=True
    )