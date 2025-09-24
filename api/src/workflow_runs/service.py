from sqlalchemy.ext.asyncio import AsyncSession
from api.src.workflow_runs.repository import WorkflowRunRepository


class WorkflowRunService:
    def __init__(self, session: AsyncSession):
        self.repository = WorkflowRunRepository(session)

    async def get_run_by_id(self, run_id: int, user_id: int):
        return await self.repository.get_by_id_and_user(run_id, user_id)

    async def get_all_runs_for_workflow(self, workflow_id: int, user_id: int):
        return await self.repository.get_all_for_workflow_and_user(workflow_id, user_id)
