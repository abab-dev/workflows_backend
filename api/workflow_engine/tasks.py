from sqlalchemy.ext.asyncio import AsyncSession

from api.src.workflows.repository import WorkflowRepository
from api.src.workflows.schemas_workflow import WorkflowContent
from api.workflow_engine.engine import WorkflowEngine


async def run_workflow_task(workflow_id: int, user_id: int, session: AsyncSession):
    print(f"Starting background task for workflow {workflow_id} for user {user_id}")
    try:
        workflow_repo = WorkflowRepository(session)
        workflow = await workflow_repo.get_by_id(workflow_id, user_id)

        if not workflow or not workflow.json_content:
            print(f"Workflow {workflow_id} not found or has no content.")
            return
        validated_content = WorkflowContent.model_validate(workflow.json_content)

        engine = WorkflowEngine(validated_content, user_id, session)
        await engine.run()
    except Exception as e:
        print(f"Error executing workflow {workflow_id}: {e}")
    finally:
        await session.close()
