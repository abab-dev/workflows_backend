from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["api.src.models", "api.workflow_engine.tasks"],
)


celery_app.conf.task_acks_late = True

celery_app.conf.update(
    task_track_started=True,
)
