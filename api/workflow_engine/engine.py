from collections import deque

from sqlalchemy.ext.asyncio import AsyncSession

from api.src.credentials.service import CredentialService
from api.src.workflows.schemas_workflow import WorkflowContent
from api.workflow_engine.nodes.registry import get_node_executor


class WorkflowEngine:
    def __init__(
        self, workflow_content: WorkflowContent, user_id: int, session: AsyncSession
    ):
        print(workflow_content)
        self.content = workflow_content
        self.nodes = {node.id: node for node in workflow_content.nodes}
        self.user_id = user_id
        self.session = session
        self.credential_service = CredentialService(session)

    async def _execute_node(self, node_id: str, input_data: dict) -> dict:
        node_config = self.nodes[node_id]
        node_type = node_config.type
        node_inputs = node_config.data.inputs

        print(f"Executing node {node_id} of type {node_type}")

        credentials = {}
        if hasattr(node_inputs, "credentialId") and node_inputs.credentialId:
            decrypted_value = await self.credential_service.get_decrypted_credential(
                node_inputs.credentialId, self.user_id
            )

            credentials["bot_token"] = decrypted_value

        ExecutorClass = get_node_executor(node_type)

        executor = ExecutorClass(node_id, node_inputs, credentials)

        return await executor.execute(input_data)

    async def run(self):
        start_node_id = self.content.startNodeId
        adjacency_list = {node.id: [] for node in self.content.nodes}
        for edge in self.content.edges:
            adjacency_list[edge.source].append(edge.target)

        execution_queue = deque([(start_node_id, {})])
        workflow_context = {}

        while execution_queue:
            current_node_id, input_data = execution_queue.popleft()

            output_data = await self._execute_node(current_node_id, input_data)
            workflow_context[current_node_id] = output_data

            for next_node_id in adjacency_list.get(current_node_id, []):
                execution_queue.append((next_node_id, output_data))

        print("Workflow execution completed.")
        return workflow_context
