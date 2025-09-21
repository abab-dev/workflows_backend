from pydantic import BaseModel, ConfigDict


class CredentialBase(BaseModel):
    name: str
    type: str


class CredentialCreate(CredentialBase):
    value: str


class CredentialResponse(CredentialBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
