import uuid

from app.database.models import Base
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class File(Base):
    __tablename__ = "storage_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    key = Column(String, unique=True, nullable=False)
    uploaded_at = Column(DateTime, default=func.now())