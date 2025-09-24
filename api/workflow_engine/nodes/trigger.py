from pydantic import BaseModel

from api.src.workflows.schemas_workflow import ManualTriggerNodeInputs
from api.workflow_engine.nodes.base import BaseNodeExecutor


class ManualTriggerNodeExecutor(BaseNodeExecutor):
    async def execute(self, input_data: dict) -> dict:
        print("Executing Manual Trigger Node")
        return {"status": "started"}

    @classmethod
    def get_input_schema(cls) -> type[BaseModel]:
        return ManualTriggerNodeInputs
