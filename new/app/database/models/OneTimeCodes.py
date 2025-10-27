import uuid

from app.database.models import Base
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class OneTimeCode(Base):
    __tablename__ = "one_time_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login_id_hash = Column(String, unique=True, nullable=False)
    fingerprint = Column(String)
    code = Column(String, nullable=False)
    accepted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
