from typing import Annotated, Literal

from pydantic import BaseModel, Field


class ManualTriggerNodeInputs(BaseModel):
    type: Literal["manual_trigger"]


class WebhookTriggerNodeInputs(BaseModel):
    type: Literal["webhook_trigger"]


class TelegramNodeInputs(BaseModel):
    type: Literal["telegram"]
    credentialId: int = Field(..., description="The ID of the credential to use")
    chat_id: str = Field(..., description="The destination Chat ID")
    message_text: str = Field(
        ..., max_length=4096, description="The text of the message to send"
    )


class LLMNodeInputs(BaseModel):
    type: Literal["llm"]
    credentialId: int
    model_name: str = Field("gemini-1.5-flash", description="The Gemini model to use")
    prompt: str = Field(..., description="The prompt to send to the LLM")


class LangGraphNodeInputs(BaseModel):
    type: Literal["langgraph"]
    credentialId: int
    model_name: str = Field("gemini-1.5-flash", description="The Gemini model to use")
    prompt: str = Field(..., description="The initial prompt for the agent")


NodeInputsUnion = Annotated[
    ManualTriggerNodeInputs
    | TelegramNodeInputs
    | LLMNodeInputs
    | LangGraphNodeInputs
    | WebhookTriggerNodeInputs,
    Field(discriminator="type"),
]


class NodeData(BaseModel):
    label: str | None = None
    inputs: NodeInputsUnion


class Node(BaseModel):
    id: str

    type: Literal["manual_trigger", "telegram", "llm", "langgraph", "webhook_trigger"]
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
