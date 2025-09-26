from api.core.config import settings
from arq.connections import RedisSettings
import api.src.models


from api.workflow_engine.tasks import run_workflow


class Worker:
    """ARQ Worker Settings."""

    functions = [run_workflow]

    redis_settings = RedisSettings.from_dsn("redis://localhost:6379")

    max_jobs = 10

    job_timeout = 300

    health_check_interval = 60
