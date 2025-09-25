from fastapi import FastAPI

from api.core.config import settings
from api.core.logging import get_logger, setup_logging
from api.src.users.routes import router as auth_router
from api.src.workflows.routes import router as workflows_router
from api.src.credentials.routes import router as credentials_router
from api.src.workflow_runs.routes import router as workflow_runs_router
from api.src.webhooks.routes import router as webhooks_router
from api.utils.migrations import run_migrations

# Set up logging configuration
setup_logging()

# Optional: Run migrations on startup
run_migrations()

# Set up logger for this module
logger = get_logger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
)

app.include_router(webhooks_router)
# Include routers
app.include_router(auth_router)
app.include_router(credentials_router)
app.include_router(workflows_router)
app.include_router(workflow_runs_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def root():
    """Root endpoint."""
    logger.debug("Root endpoint called")
    return {"message": "Welcome to Hero API!"}
