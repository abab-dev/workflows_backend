from typing import Annotated, Literal

from pydantic import BaseModel, Field


class TelegramNodeInputs(BaseModel):
    credentialId: int = Field(..., description="The ID of the credential to use")
    chat_id: str = Field(..., description="The destination Chat ID")
    message_text: str = Field(
        ..., max_length=4096, description="The text of the message to send"
    )


class NodeData(BaseModel):
    label: str | None = None
    inputs: TelegramNodeInputs


class Node(BaseModel):
    id: str
    type: Literal["telegram"]
    position: dict
    data: NodeData


class Edge(BaseModel):
    id: str
    source: str
    target: str


class WorkflowContent(BaseModel):
    startNodeId: str = Field(..., description="The ID of the starting node")
    nodes: list[Node]
    edges: list[Edge]
