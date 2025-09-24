from api.workflow_engine.nodes.telegram import TelegramNodeExecutor

NODE_EXECUTORS = {
    "telegram": TelegramNodeExecutor,
}


def get_node_executor(node_type: str):
    executor = NODE_EXECUTORS.get(node_type)
    if not executor:
        raise ValueError(f"Unsupported node type: {node_type}")
    return executor
