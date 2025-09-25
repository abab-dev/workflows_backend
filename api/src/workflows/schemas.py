from datetime import datetime

from pydantic import BaseModel, ConfigDict
import uuid

from .schemas_workflow import WorkflowContent


class WorkflowBase(BaseModel):
    name: str
    json_content: WorkflowContent | None = None


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(BaseModel):
    name: str | None = None
    json_content: WorkflowContent | None = None


class WorkflowResponse(WorkflowBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    webhook_token: uuid.UUID
    created_at: datetime
    updated_at: datetime
