from api.workflow_engine.nodes.telegram import TelegramNodeExecutor
from api.workflow_engine.nodes.trigger import ManualTriggerNodeExecutor
from api.workflow_engine.nodes.llm import LLMNodeExecutor
from api.workflow_engine.nodes.langgraph import LangGraphNodeExecutor

NODE_EXECUTORS = {
    "manual_trigger": ManualTriggerNodeExecutor,
    "telegram": TelegramNodeExecutor,
    "llm": LLMNodeExecutor,
    "langgraph": LangGraphNodeExecutor,
}


def get_node_executor(node_type: str):
    executor = NODE_EXECUTORS.get(node_type)
    if not executor:
        raise ValueError(f"Unsupported node type: {node_type}")
    return executor
