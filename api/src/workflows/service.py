from sqlalchemy.ext.asyncio import AsyncSession

from api.src.workflows.repository import WorkflowRepository
from api.src.workflows.schemas import WorkflowCreate, WorkflowUpdate


class WorkflowService:
    def __init__(self, session: AsyncSession):
        self.repository = WorkflowRepository(session)

    async def create_workflow(self, workflow_data: WorkflowCreate, user_id: int):
        return await self.repository.create(workflow_data, user_id)

    async def get_workflow(self, workflow_id: int, user_id: int):
        return await self.repository.get_by_id(workflow_id, user_id)

    async def get_all_workflows(self, user_id: int):
        return await self.repository.get_all_by_user_id(user_id)

    async def update_workflow(
        self, workflow_id: int, workflow_data: WorkflowUpdate, user_id: int
    ):
        return await self.repository.update(workflow_id, workflow_data, user_id)

    async def delete_workflow(self, workflow_id: int, user_id: int):
        await self.repository.delete(workflow_id, user_id)
