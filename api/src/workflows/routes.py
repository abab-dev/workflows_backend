from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_session
from api.core.security import get_current_user
from api.src.users.models import User
from api.src.workflows.schemas import (
    WorkflowCreate,
    WorkflowResponse,
    WorkflowUpdate,
)
from api.src.workflows.service import WorkflowService

router = APIRouter(prefix="/workflows", tags=["workflows"])


def get_workflow_service(
    session: AsyncSession = Depends(get_session),
) -> WorkflowService:
    return WorkflowService(session)


@router.post("/", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    workflow_data: WorkflowCreate,
    service: WorkflowService = Depends(get_workflow_service),
    current_user: User = Depends(get_current_user),
) -> WorkflowResponse:
    return await service.create_workflow(workflow_data, current_user.id)


@router.get("/", response_model=list[WorkflowResponse])
async def get_all_workflows(
    service: WorkflowService = Depends(get_workflow_service),
    current_user: User = Depends(get_current_user),
) -> list[WorkflowResponse]:
    return await service.get_all_workflows(current_user.id)


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: int,
    service: WorkflowService = Depends(get_workflow_service),
    current_user: User = Depends(get_current_user),
) -> WorkflowResponse:
    return await service.get_workflow(workflow_id, current_user.id)


@router.patch("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: int,
    workflow_data: WorkflowUpdate,
    service: WorkflowService = Depends(get_workflow_service),
    current_user: User = Depends(get_current_user),
) -> WorkflowResponse:
    return await service.update_workflow(workflow_id, workflow_data, current_user.id)


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(
    workflow_id: int,
    service: WorkflowService = Depends(get_workflow_service),
    current_user: User = Depends(get_current_user),
) -> None:
    await service.delete_workflow(workflow_id, current_user.id)
