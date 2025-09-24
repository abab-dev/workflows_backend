from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.core.exceptions import NotFoundException
from api.src.workflow_runs.models import WorkflowRun
from api.src.workflows.models import Workflow


class WorkflowRunRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, workflow_id: int) -> WorkflowRun:
        run = WorkflowRun(workflow_id=workflow_id, status="PENDING")
        self.session.add(run)
        await self.session.commit()
        await self.session.refresh(run)
        return run

    async def get_by_id_and_user(self, run_id: int, user_id: int) -> WorkflowRun:
        query = (
            select(WorkflowRun)
            .join(WorkflowRun.workflow)
            .where(WorkflowRun.id == run_id, Workflow.user_id == user_id)
        )
        result = await self.session.execute(query)
        run = result.scalar_one_or_none()
        if not run:
            raise NotFoundException(f"Workflow run with id {run_id} not found")
        return run

    async def get_all_for_workflow_and_user(
        self, workflow_id: int, user_id: int
    ) -> list[WorkflowRun]:
        workflow_query = select(Workflow).where(
            Workflow.id == workflow_id, Workflow.user_id == user_id
        )
        workflow_result = await self.session.execute(workflow_query)
        if not workflow_result.scalar_one_or_none():
            raise NotFoundException(f"Workflow with id {workflow_id} not found")

        query = select(WorkflowRun).where(WorkflowRun.workflow_id == workflow_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update_status(
        self, run_id: int, status: str, logs: str | None
    ) -> WorkflowRun:
        run = await self.get_by_id(run_id)
        query = (
            update(WorkflowRun)
            .where(WorkflowRun.id == run_id)
            .values(status=status, logs=logs, finished_at=datetime.utcnow())
        )
        await self.session.execute(query)
        await self.session.commit()
        return await self.get_by_id(run_id)

    async def get_by_id(self, run_id: int) -> WorkflowRun:
        query = select(WorkflowRun).where(WorkflowRun.id == run_id)
        result = await self.session.execute(query)
        run = result.scalar_one_or_none()
        if not run:
            raise NotFoundException(f"Workflow run with id {run_id} not found")
        return run
