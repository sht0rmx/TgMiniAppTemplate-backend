import uuid

from app.database.models import Base
from sqlalchemy import Column, ForeignKey, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(30))
    api_key_hash = Column(String)
    role = Column(String, default="user")
    banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
