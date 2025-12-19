"""
FastAPI server for Browser-Use API.
Provides HTTP endpoints for dynamic browser automation tasks.
"""
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from uuid import uuid4

import httpx
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from api.auth import validate_api_key
from api.config import CHROME_CDP_URL
from api.database import db, init_database
from api.models import (
    TaskRequest,
    TaskResponse,
    TaskStatus,
    TaskListResponse,
    HealthResponse,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for FastAPI app.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Browser-Use API Server...")
    await init_database()
    logger.info("Database initialized")

    yield

    # Shutdown
    logger.info("Shutting down Browser-Use API Server...")


# Create FastAPI app
app = FastAPI(
    title="Browser-Use API",
    description="HTTP API for dynamic browser automation tasks using browser-use",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Enhanced health check endpoint.
    Verifies Chrome CDP, database, and queue status.
    """
    health = {
        "api": "healthy",
        "chrome_cdp": "unknown",
        "database": "unknown",
        "queue_size": 0,
    }

    # Check Chrome CDP
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CHROME_CDP_URL}/json/version",
                timeout=2.0
            )
            health["chrome_cdp"] = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception as e:
        logger.error(f"Chrome CDP health check failed: {e}")
        health["chrome_cdp"] = "unhealthy"

    # Check Database
    try:
        # Simple query to verify database is accessible
        test_task = await db.get_task("health-check-test")
        health["database"] = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health["database"] = "unhealthy"

    # Determine overall health
    is_healthy = all(
        v == "healthy" or k == "queue_size"
        for k, v in health.items()
    )

    status_code = 200 if is_healthy else 503

    return JSONResponse(content=health, status_code=status_code)


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(validate_api_key)]
)
async def create_task(request: TaskRequest):
    """
    Create a new browser automation task.

    The task is queued for execution and a task_id is returned immediately.
    Use GET /tasks/{task_id} to check status and results.
    """
    # Check if Chrome CDP is available before accepting task
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CHROME_CDP_URL}/json/version",
                timeout=2.0
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=503,
                    detail="Chrome CDP not responding. Start Chrome with: ./scripts/start_chrome_debug.sh"
                )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Chrome CDP not available. Start Chrome with: ./scripts/start_chrome_debug.sh"
        )

    # Generate task ID
    task_id = str(uuid4())

    # Create task in database
    task_data = await db.create_task(
        task_id=task_id,
        url=str(request.url),
        task_description=request.task_description,
        form_data=request.form_data,
        callback_url=str(request.callback_url) if request.callback_url else None,
        timeout=request.timeout
    )

    logger.info(f"Created task {task_id}: {request.task_description[:50]}...")

    # Note: In Phase 3, we'll add the task to the queue here
    # For now, just return the task response

    return TaskResponse(
        task_id=task_data["task_id"],
        status=task_data["status"],
        queue_position=None,  # Will be implemented in Phase 3
        created_at=task_data["created_at"]
    )


@app.get(
    "/tasks/{task_id}",
    response_model=TaskStatus,
    dependencies=[Depends(validate_api_key)]
)
async def get_task(task_id: str):
    """
    Get status and results of a specific task.
    """
    task = await db.get_task(task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return TaskStatus(
        task_id=task["task_id"],
        status=task["status"],
        url=task["url"],
        task_description=task["task_description"],
        result=task["result"],
        error=task["error"],
        created_at=datetime.fromisoformat(task["created_at"]),
        started_at=datetime.fromisoformat(task["started_at"]) if task["started_at"] else None,
        completed_at=datetime.fromisoformat(task["completed_at"]) if task["completed_at"] else None,
    )


@app.get(
    "/tasks",
    response_model=TaskListResponse,
    dependencies=[Depends(validate_api_key)]
)
async def list_tasks(
    status: str = None,
    limit: int = 50,
    offset: int = 0
):
    """
    List all tasks with optional filtering and pagination.

    Query parameters:
    - status: Filter by task status (queued, running, completed, failed, timeout)
    - limit: Maximum number of tasks to return (default: 50, max: 100)
    - offset: Number of tasks to skip (default: 0)
    """
    # Validate limit
    if limit > 100:
        limit = 100
    if limit < 1:
        limit = 1

    tasks_data, total = await db.list_tasks(status=status, limit=limit, offset=offset)

    tasks = [
        TaskStatus(
            task_id=task["task_id"],
            status=task["status"],
            url=task["url"],
            task_description=task["task_description"],
            result=task["result"],
            error=task["error"],
            created_at=datetime.fromisoformat(task["created_at"]),
            started_at=datetime.fromisoformat(task["started_at"]) if task["started_at"] else None,
            completed_at=datetime.fromisoformat(task["completed_at"]) if task["completed_at"] else None,
        )
        for task in tasks_data
    ]

    return TaskListResponse(
        tasks=tasks,
        total=total,
        limit=limit,
        offset=offset
    )


if __name__ == "__main__":
    import uvicorn
    from api.config import API_HOST, API_PORT

    uvicorn.run(
        "api.server:app",
        host=API_HOST,
        port=API_PORT,
        log_config="logging.yaml",
        reload=True
    )
