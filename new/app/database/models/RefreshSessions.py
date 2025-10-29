import uuid

from app.database.models import Base
from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class RefreshSession(Base):
    __tablename__ = "refresh_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    refresh_token_hash = Column(String, unique=True, nullable=False)
    fingerprint = Column(String)
    ip = Column(String)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())