from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.exceptions import NotFoundException
from api.src.workflows.models import Workflow
from api.src.workflows.schemas import WorkflowCreate, WorkflowUpdate
import uuid


class WorkflowRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, workflow_data: WorkflowCreate, user_id: int) -> Workflow:
        workflow = Workflow(**workflow_data.model_dump(), user_id=user_id)
        self.session.add(workflow)
        await self.session.commit()
        await self.session.refresh(workflow)
        return workflow

    async def get_by_id(self, workflow_id: int, user_id: int) -> Workflow:
        query = select(Workflow).where(
            Workflow.id == workflow_id, Workflow.user_id == user_id
        )
        result = await self.session.execute(query)
        workflow = result.scalar_one_or_none()

        if not workflow:
            raise NotFoundException(f"Workflow with id {workflow_id} not found")
        return workflow

    async def get_all_by_user_id(self, user_id: int) -> list[Workflow]:
        query = select(Workflow).where(Workflow.user_id == user_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(
        self, workflow_id: int, workflow_data: WorkflowUpdate, user_id: int
    ) -> Workflow:
        await self.get_by_id(workflow_id, user_id)

        update_data = workflow_data.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_id(workflow_id, user_id)

        query = (
            update(Workflow)
            .where(Workflow.id == workflow_id, Workflow.user_id == user_id)
            .values(**update_data)
        )
        await self.session.execute(query)
        await self.session.commit()

        return await self.get_by_id(workflow_id, user_id)

    async def delete(self, workflow_id: int, user_id: int) -> None:
        await self.get_by_id(workflow_id, user_id)

        query = delete(Workflow).where(
            Workflow.id == workflow_id, Workflow.user_id == user_id
        )
        await self.session.execute(query)
        await self.session.commit()

    async def get_by_webhook_token(self, token: uuid.UUID) -> Workflow:
        query = select(Workflow).where(Workflow.webhook_token == token)
        result = await self.session.execute(query)
        workflow = result.scalar_one_or_none()

        if not workflow:
            raise NotFoundException("Workflow with the provided token not found")
        return workflow
