from abc import ABC, abstractmethod
from pydantic import BaseModel


class BaseNodeExecutor(ABC):
    def __init__(self, node_id: str, parameters: BaseModel, credentials: dict):
        self.node_id = node_id
        self.parameters = parameters
        self.credentials = credentials

    @abstractmethod
    async def execute(self, input_data: dict) -> dict:
        pass

    @classmethod
    @abstractmethod
    def get_input_schema(cls) -> type[BaseModel]:
        """Returns the Pydantic model for the node's inputs."""
        pass
