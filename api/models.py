"""
Pydantic models for API request/response validation.
"""
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator


class TaskRequest(BaseModel):
    """Request model for creating a new browser automation task."""

    url: HttpUrl = Field(
        ...,
        description="The URL to navigate to for the task"
    )
    task_description: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Natural language description of what the browser should do"
    )
    form_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Optional form data to be used by the agent"
    )
    callback_url: Optional[HttpUrl] = Field(
        None,
        description="Optional webhook URL to call when task completes"
    )
    timeout: int = Field(
        default=300,
        ge=30,
        le=3600,
        description="Task timeout in seconds (30s to 1 hour)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com/application-form",
                "task_description": "Fill in the contact form with the provided information and submit it",
                "form_data": {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "message": "Hello, I'm interested in your services"
                },
                "callback_url": "http://n8n:5678/webhook/task-complete",
                "timeout": 300
            }
        }


class TaskResponse(BaseModel):
    """Response model for task creation."""

    task_id: str
    status: str
    queue_position: Optional[int] = None
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "queued",
                "queue_position": 3,
                "created_at": "2025-12-19T10:30:00Z"
            }
        }


class TaskStatus(BaseModel):
    """Response model for task status queries."""

    task_id: str
    status: str
    url: Optional[str] = None
    task_description: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "completed",
                "url": "https://example.com/form",
                "task_description": "Fill in the contact form",
                "result": "Task completed successfully. Form submitted.",
                "error": None,
                "created_at": "2025-12-19T10:30:00Z",
                "started_at": "2025-12-19T10:30:05Z",
                "completed_at": "2025-12-19T10:32:15Z"
            }
        }


class TaskListResponse(BaseModel):
    """Response model for listing tasks."""

    tasks: list[TaskStatus]
    total: int
    limit: int
    offset: int

    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [],
                "total": 42,
                "limit": 50,
                "offset": 0
            }
        }


class QueueStatus(BaseModel):
    """Response model for queue status."""

    queue_length: int
    current_task: Optional[Dict[str, Any]] = None
    estimated_completion: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "queue_length": 5,
                "current_task": {
                    "task_id": "550e8400-e29b-41d4-a716-446655440000",
                    "started_at": "2025-12-19T10:30:00Z"
                },
                "estimated_completion": "2025-12-19T11:45:00Z"
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check."""

    api: str
    chrome_cdp: str
    database: str
    queue_size: int

    class Config:
        json_schema_extra = {
            "example": {
                "api": "healthy",
                "chrome_cdp": "healthy",
                "database": "healthy",
                "queue_size": 5
            }
        }


class CallbackPayload(BaseModel):
    """Payload sent to callback webhooks when task completes."""

    task_id: str
    status: str
    result: Optional[str] = None
    error: Optional[str] = None
    completed_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "completed",
                "result": "Task completed successfully",
                "error": None,
                "completed_at": "2025-12-19T10:32:15Z"
            }
        }
