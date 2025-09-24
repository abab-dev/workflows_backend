from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_session
from api.core.security import get_current_user
from api.src.users.models import User
from api.src.workflow_runs.schemas import WorkflowRunResponse
from api.src.workflow_runs.service import WorkflowRunService


router = APIRouter(tags=["workflow_runs"])


def get_workflow_run_service(
    session: AsyncSession = Depends(get_session),
) -> WorkflowRunService:
    return WorkflowRunService(session)


@router.get("/workflows/{workflow_id}/runs", response_model=list[WorkflowRunResponse])
async def get_all_runs_for_workflow(
    workflow_id: int,
    service: WorkflowRunService = Depends(get_workflow_run_service),
    current_user: User = Depends(get_current_user),
):
    return await service.get_all_runs_for_workflow(workflow_id, current_user.id)


@router.get("/workflow-runs/{run_id}", response_model=WorkflowRunResponse)
async def get_workflow_run(
    run_id: int,
    service: WorkflowRunService = Depends(get_workflow_run_service),
    current_user: User = Depends(get_current_user),
):
    return await service.get_run_by_id(run_id, current_user.id)
