import os
from dotenv import load_dotenv
from datetime import date
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel

from api.src.workflows.schemas_workflow import LangGraphNodeInputs
from api.workflow_engine.nodes.base import BaseNodeExecutor

load_dotenv()


@tool
def get_current_date(just_the_year: bool = False) -> str:
    """Returns the current date. If just_the_year is true, returns only the year."""
    today = date.today()
    if just_the_year:
        return str(today.year)
    return today.isoformat()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


class LangGraphNodeExecutor(BaseNodeExecutor):
    async def execute(self, input_data: dict) -> dict:
        print("Executing LangGraph Agent Node")
        api_key = self.credentials.get("google_api_key")
        if not api_key:
            raise ValueError("Missing Google API Key in credentials for LangGraph node")
        model = ChatGoogleGenerativeAI(
            model=self.parameters.model_name, google_api_key=api_key
        )
        tools = [get_current_date]
        model_with_tools = model.bind_tools(tools)

        graph_builder = StateGraph(AgentState)

        def chatbot(state: AgentState):
            return {"messages": [model_with_tools.invoke(state["messages"])]}

        graph_builder.add_node("chatbot", chatbot)
        graph_builder.add_node("tools", ToolNode(tools))
        graph_builder.set_entry_point("chatbot")

        def router(state: AgentState):
            tool_calls = state["messages"][-1].tool_calls
            if not tool_calls:
                return "end"
            return "tools"

        graph_builder.add_conditional_edges(
            "chatbot", router, {"end": "__end__", "tools": "tools"}
        )
        graph_builder.add_edge("tools", "chatbot")

        graph = graph_builder.compile()

        initial_prompt = self.parameters.prompt
        final_state = await graph.ainvoke(
            {"messages": [HumanMessage(content=initial_prompt)]}
        )

        final_response = final_state["messages"][-1].content
        print(f"LangGraph Agent Final Response: {final_response}")

        return {"final_response": final_response}

    @classmethod
    def get_input_schema(cls) -> type[BaseModel]:
        return LangGraphNodeInputs
