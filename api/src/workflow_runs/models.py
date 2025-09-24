from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from api.core.database import Base


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    status = Column(String(50), nullable=False, default="PENDING")
    logs = Column(Text, nullable=True)

    started_at = Column(DateTime, default=func.now())
    finished_at = Column(DateTime, nullable=True)

    workflow = relationship("Workflow")
