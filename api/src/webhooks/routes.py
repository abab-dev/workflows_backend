import uuid
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession


from api.core.database import async_session
from api.src.workflows.repository import WorkflowRepository
from api.workflow_engine.tasks import run_workflow_task

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/{token}")
async def trigger_webhook(
    token: uuid.UUID,
    request: Request,
):
    """Public endpoint to trigger a workflow via Celery."""

    async with async_session() as session:
        workflow_repo = WorkflowRepository(session)
        workflow = await workflow_repo.get_by_webhook_token(token)

    payload = await request.json()

    run_workflow_task.delay(
        workflow_id=workflow.id,
        user_id=workflow.user_id,
        initial_payload=payload,
    )

    return {"status": "accepted"}
