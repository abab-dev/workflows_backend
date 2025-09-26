import json
from api.core.database import async_session
from api.src.workflows.repository import WorkflowRepository
from api.src.workflows.schemas_workflow import WorkflowContent
from api.src.workflow_runs.repository import WorkflowRunRepository
from api.workflow_engine.engine import WorkflowEngine


async def run_workflow(
    ctx,
    workflow_id: int,
    user_id: int,
    initial_payload: dict | None = None,
):
    async with async_session() as session:
        run_repo = WorkflowRunRepository(session)
        run = await run_repo.create(workflow_id)
        job_id = ctx.get("job_id")
        print(f"Starting ARQ job {job_id} for workflow {workflow_id}, run {run.id}")

        try:
            workflow_repo = WorkflowRepository(session)
            workflow = await workflow_repo.get_by_id(workflow_id, user_id)

            if not workflow or not workflow.json_content:
                raise ValueError(f"Workflow {workflow_id} not found or has no content.")

            validated_content = WorkflowContent.model_validate(workflow.json_content)
            engine = WorkflowEngine(validated_content, user_id, session)
            result_context = await engine.run(initial_payload=initial_payload)

            logs = json.dumps(result_context, indent=2)
            await run_repo.update_status(run.id, "SUCCESS", logs)
            print(f"Finished ARQ job {job_id}, run {run.id} successfully.")

        except Exception as e:
            print(f"Error in ARQ job {job_id}, run {run.id}: {e}")
            await run_repo.update_status(run.id, "FAILED", str(e))
            raise
