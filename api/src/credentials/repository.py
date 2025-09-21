from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.exceptions import NotFoundException
from api.src.credentials.models import Credential


class CredentialRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, credential: Credential) -> Credential:
        self.session.add(credential)
        await self.session.commit()
        await self.session.refresh(credential)
        return credential

    async def get_by_id(self, credential_id: int, user_id: int) -> Credential | None:
        query = select(Credential).where(
            Credential.id == credential_id, Credential.user_id == user_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all_by_user_id(self, user_id: int) -> list[Credential]:
        query = select(Credential).where(Credential.user_id == user_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def delete(self, credential_id: int, user_id: int) -> None:
        credential = await self.get_by_id(credential_id, user_id)
        if not credential:
            raise NotFoundException(f"Credential with id {credential_id} not found")

        query = delete(Credential).where(
            Credential.id == credential_id, Credential.user_id == user_id
        )
        await self.session.execute(query)
        await self.session.commit()
