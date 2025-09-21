from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import get_session
from api.core.security import get_current_user
from api.src.users.models import User
from api.src.credentials.schemas import CredentialCreate, CredentialResponse
from api.src.credentials.service import CredentialService

router = APIRouter(prefix="/credentials", tags=["credentials"])


def get_credential_service(
    session: AsyncSession = Depends(get_session),
) -> CredentialService:
    return CredentialService(session)


@router.post(
    "/", response_model=CredentialResponse, status_code=status.HTTP_201_CREATED
)
async def create_credential(
    credential_data: CredentialCreate,
    service: CredentialService = Depends(get_credential_service),
    current_user: User = Depends(get_current_user),
) -> CredentialResponse:
    return await service.create_credential(credential_data, current_user.id)


@router.get("/", response_model=list[CredentialResponse])
async def get_all_credentials(
    service: CredentialService = Depends(get_credential_service),
    current_user: User = Depends(get_current_user),
) -> list[CredentialResponse]:
    return await service.get_all_credentials(current_user.id)


@router.delete("/{credential_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_credential(
    credential_id: int,
    service: CredentialService = Depends(get_credential_service),
    current_user: User = Depends(get_current_user),
) -> None:
    await service.delete_credential(credential_id, current_user.id)
