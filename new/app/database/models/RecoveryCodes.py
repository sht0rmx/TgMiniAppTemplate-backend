import uuid

from app.database.models import Base
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class RecoveryCode(Base):
    __tablename__ = "recovery_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    code_hash = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())