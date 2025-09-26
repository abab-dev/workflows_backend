from datetime import datetime
import uuid


from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    UUID,
    func,
)
from sqlalchemy.orm import relationship

from api.core.database import Base


class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    json_content = Column(JSON, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    webhook_token = Column(
        UUID(as_uuid=True), unique=True, default=uuid.uuid4, index=True
    )

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    owner = relationship("User", back_populates="workflows")
