from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WorkflowBase(BaseModel):
    name: str
    json_content: dict | None = None


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(BaseModel):
    name: str | None = None
    json_content: dict | None = None


class WorkflowResponse(WorkflowBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
