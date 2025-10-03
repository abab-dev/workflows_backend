from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from api.core.config import settings
from api.core.logging import get_logger, setup_logging
from api.src.users.routes import router as auth_router
from api.src.workflows.routes import router as workflows_router
from api.src.credentials.routes import router as credentials_router
from api.src.workflow_runs.routes import router as workflow_runs_router
from api.src.webhooks.routes import router as webhooks_router
from api.utils.migrations import run_migrations
from api.core.redis import (
    create_redis_pool,
    close_redis_pool,
)


setup_logging()


run_migrations()


logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_redis_pool()
    yield

    await close_redis_pool()


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(webhooks_router)

app.include_router(auth_router)
app.include_router(credentials_router)
app.include_router(workflows_router)
app.include_router(workflow_runs_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def root():
    logger.debug("Root endpoint called")
    return {"message": "Welcome to Hero API!"}
