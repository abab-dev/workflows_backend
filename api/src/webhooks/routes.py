import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_session
from api.src.workflows.repository import WorkflowRepository
from api.workflow_engine.tasks import run_workflow_task

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/{token}")
async def trigger_webhook(
    token: uuid.UUID,
    request: Request,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    """Public endpoint to trigger a workflow via its unique webhook token."""
    workflow_repo = WorkflowRepository(session)
    workflow = await workflow_repo.get_by_webhook_token(token)

    payload = await request.json()

    background_tasks.add_task(
        run_workflow_task,
        workflow.id,
        workflow.user_id,
        session,
        initial_payload=payload,
    )

    return {"status": "accepted"}
