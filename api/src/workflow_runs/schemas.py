from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WorkflowRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    workflow_id: int
    status: str
    logs: str | None = None
    started_at: datetime
    finished_at: datetime | None = None
