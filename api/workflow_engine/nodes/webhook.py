from pydantic import BaseModel
from api.src.workflows.schemas_workflow import WebhookTriggerNodeInputs
from api.workflow_engine.nodes.base import BaseNodeExecutor


class WebhookTriggerNodeExecutor(BaseNodeExecutor):
    async def execute(self, input_data: dict) -> dict:
        print("Executing Webhook Trigger Node")

        return {"webhook_data": input_data}

    @classmethod
    def get_input_schema(cls) -> type[BaseModel]:
        return WebhookTriggerNodeInputs
