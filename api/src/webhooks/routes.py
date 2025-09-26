import uuid
import arq
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import async_session
from api.src.workflows.repository import WorkflowRepository
from api.core.redis import get_redis_pool


router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/{token}")
async def trigger_webhook(
    token: uuid.UUID,
    request: Request,
    redis: arq.ArqRedis = Depends(get_redis_pool),
):
    async with async_session() as session:
        workflow_repo = WorkflowRepository(session)
        workflow = await workflow_repo.get_by_webhook_token(token)

    payload = await request.json()

    await redis.enqueue_job(
        "run_workflow",
        workflow_id=workflow.id,
        user_id=workflow.user_id,
        initial_payload=payload,
    )

    return {"status": "accepted"}
