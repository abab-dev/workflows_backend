from collections import deque
from sqlalchemy.ext.asyncio import AsyncSession

from api.src.credentials.service import CredentialService

from api.src.workflows.schemas_workflow import NodeData, WorkflowContent
from api.workflow_engine.expression_parser import resolve_parameters
from api.workflow_engine.nodes.registry import get_node_executor


class WorkflowEngine:
    def __init__(
        self, workflow_content: WorkflowContent, user_id: int, session: AsyncSession
    ):
        self.content = workflow_content
        self.nodes = {node.id: node for node in workflow_content.nodes}
        self.user_id = user_id
        self.session = session
        self.credential_service = CredentialService(session)
        self.workflow_context = {"nodes": {}}

    async def _execute_node(self, node_id: str, input_data: dict) -> dict:
        node_config = self.nodes[node_id]
        node_type = node_config.type

        print(f"Executing node {node_id} of type {node_type}")

        raw_data = node_config.data.model_dump()

        resolved_data = resolve_parameters(raw_data, self.workflow_context)

        validated_data = NodeData.model_validate(resolved_data)
        validated_inputs = validated_data.inputs

        credential_id = (
            validated_inputs.credentialId
            if hasattr(validated_inputs, "credentialId")
            else None
        )

        credentials = {}
        if credential_id:
            decrypted_value = await self.credential_service.get_decrypted_credential(
                credential_id, self.user_id
            )
            if node_type in ["llm", "langgraph"]:
                credentials["google_api_key"] = decrypted_value
            elif node_type == "telegram":
                credentials["bot_token"] = decrypted_value

        ExecutorClass = get_node_executor(node_type)
        executor = ExecutorClass(node_id, validated_inputs, credentials)
        return await executor.execute(input_data)

    async def run(self, initial_payload: dict | None = None):
        start_node_id = self.content.startNodeId
        adjacency_list = {node.id: [] for node in self.content.nodes}
        for edge in self.content.edges:
            adjacency_list[edge.source].append(edge.target)

        start_node_input = initial_payload if initial_payload is not None else {}
        execution_queue = deque([(start_node_id, start_node_input)])

        while execution_queue:
            current_node_id, input_data = execution_queue.popleft()

            output_data = await self._execute_node(current_node_id, input_data)
            self.workflow_context["nodes"][current_node_id] = {"output": output_data}

            for next_node_id in adjacency_list.get(current_node_id, []):
                execution_queue.append((next_node_id, output_data))

        print("Workflow execution completed.")
        return self.workflow_context
