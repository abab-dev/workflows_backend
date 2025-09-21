from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.config import settings
from api.core.exceptions import NotFoundException
from api.src.credentials.models import Credential
from api.src.credentials.repository import CredentialRepository
from api.src.credentials.schemas import CredentialCreate


class CredentialService:
    def __init__(self, session: AsyncSession):
        self.repository = CredentialRepository(session)
        self.fernet = Fernet(settings.ENCRYPTION_KEY.encode())

    def _encrypt(self, value: str) -> str:
        return self.fernet.encrypt(value.encode()).decode()

    def _decrypt(self, encrypted_value: str) -> str:
        return self.fernet.decrypt(encrypted_value.encode()).decode()

    async def create_credential(self, credential_data: CredentialCreate, user_id: int):
        encrypted_value = self._encrypt(credential_data.value)
        db_credential = Credential(
            name=credential_data.name,
            type=credential_data.type,
            encrypted_value=encrypted_value,
            user_id=user_id,
        )
        return await self.repository.create(db_credential)

    async def get_all_credentials(self, user_id: int):
        return await self.repository.get_all_by_user_id(user_id)

    async def delete_credential(self, credential_id: int, user_id: int):
        await self.repository.delete(credential_id, user_id)

    async def get_decrypted_credential(self, credential_id: int, user_id: int) -> str:
        credential = await self.repository.get_by_id(credential_id, user_id)
        if not credential:
            raise NotFoundException("Credential not found")
        return self._decrypt(credential.encrypted_value)
