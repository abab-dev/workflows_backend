from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from api.src.workflows.schemas_workflow import LLMNodeInputs
from api.workflow_engine.nodes.base import BaseNodeExecutor


class LLMNodeExecutor(BaseNodeExecutor):
    async def execute(self, input_data: dict) -> dict:
        print("Executing Simple Gemini LLM Node")
        model = ChatGoogleGenerativeAI(model=self.parameters.model_name)

        prompt = self.parameters.prompt
        message = HumanMessage(content=prompt)

        response = await model.ainvoke([message])

        response_text = response.content
        print(f"Gemini Response: {response_text}")

        return {"response": response_text}

    @classmethod
    def get_input_schema(cls) -> type[BaseModel]:
        return LLMNodeInputs
