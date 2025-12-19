"""
Task queue and background worker for browser automation.
Executes tasks using browser-use Agent with Chrome CDP connection.
"""
import asyncio
import logging
import json
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

import httpx
from browser_use import Agent, Browser, ChatBrowserUse

from api.config import (
    CHROME_CDP_URL,
    WEBHOOK_RETRY_ATTEMPTS,
    WEBHOOK_RETRY_DELAY,
    WEBHOOK_TIMEOUT,
)
from api.database import db
from api.models import CallbackPayload

logger = logging.getLogger("api")


class TaskQueue:
    """
    Manages the task queue and background worker.
    Processes tasks sequentially using browser-use Agent.
    """

    def __init__(self):
        self.queue: asyncio.Queue = asyncio.Queue()
        self.current_task_id: Optional[str] = None
        self.worker_task: Optional[asyncio.Task] = None
        self.running = False

    async def start(self):
        """Start the background worker."""
        if self.running:
            logger.warning("Task queue worker already running")
            return

        self.running = True
        self.worker_task = asyncio.create_task(self._worker())
        logger.info("Task queue worker started")

    async def stop(self):
        """Stop the background worker gracefully."""
        logger.info("Stopping task queue worker...")
        self.running = False

        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                pass

        logger.info("Task queue worker stopped")

    async def add_task(self, task_id: str):
        """Add a task to the queue."""
        await self.queue.put(task_id)
        logger.info(f"Task {task_id} added to queue (position: {self.queue.qsize()})")

    def get_queue_size(self) -> int:
        """Get current queue size."""
        return self.queue.qsize()

    def get_current_task(self) -> Optional[Dict[str, Any]]:
        """Get currently executing task info."""
        if self.current_task_id:
            return {"task_id": self.current_task_id}
        return None

    async def _worker(self):
        """
        Background worker that processes tasks from the queue.
        Runs continuously until stopped.
        """
        logger.info("Task queue worker loop started")

        while self.running:
            try:
                # Wait for a task (with timeout to allow checking self.running)
                try:
                    task_id = await asyncio.wait_for(
                        self.queue.get(),
                        timeout=1.0
                    )
                except asyncio.TimeoutError:
                    continue

                self.current_task_id = task_id
                logger.info(f"Processing task {task_id}")

                # Execute the task
                await self._execute_task(task_id)

                self.current_task_id = None
                self.queue.task_done()

            except asyncio.CancelledError:
                logger.info("Worker task cancelled")
                break
            except Exception as e:
                logger.error(f"Error in worker loop: {e}", exc_info=True)
                self.current_task_id = None

        logger.info("Task queue worker loop ended")

    async def _execute_task(self, task_id: str):
        """
        Execute a single task using browser-use Agent.

        Args:
            task_id: The UUID of the task to execute
        """
        started_at = datetime.utcnow()

        try:
            # Get task from database
            task = await db.get_task(task_id)
            if not task:
                logger.error(f"Task {task_id} not found in database")
                return

            # Update status to running
            await db.update_status(
                task_id=task_id,
                status="running",
                started_at=started_at
            )
            logger.info(f"Task {task_id} status updated to 'running'")

            # Parse form_data from JSON string
            form_data = {}
            if task["form_data"]:
                try:
                    form_data = json.loads(task["form_data"])
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON in form_data for task {task_id}")

            # Build task description with form data context
            task_description = task["task_description"]
            if form_data:
                task_description += f"\n\nForm data to use: {json.dumps(form_data, indent=2)}"

            # Execute browser automation
            result = await self._run_browser_task(
                task_id=task_id,
                url=task["url"],
                task_description=task_description,
                timeout=task["timeout"]
            )

            # Update status to completed
            completed_at = datetime.utcnow()
            await db.update_status(
                task_id=task_id,
                status="completed",
                completed_at=completed_at,
                result=result
            )
            logger.info(f"Task {task_id} completed successfully")

            # Send callback if provided
            if task["callback_url"]:
                await self._send_callback(
                    task_id=task_id,
                    callback_url=task["callback_url"],
                    status="completed",
                    result=result,
                    error=None,
                    completed_at=completed_at
                )

        except asyncio.TimeoutError:
            # Task exceeded timeout
            completed_at = datetime.utcnow()
            error_msg = f"Task exceeded timeout of {task['timeout']} seconds"
            logger.warning(f"Task {task_id} timed out")

            await db.update_status(
                task_id=task_id,
                status="timeout",
                completed_at=completed_at,
                error=error_msg
            )

            # Send callback for timeout
            if task.get("callback_url"):
                await self._send_callback(
                    task_id=task_id,
                    callback_url=task["callback_url"],
                    status="timeout",
                    result=None,
                    error=error_msg,
                    completed_at=completed_at
                )

        except Exception as e:
            # Task failed with error
            completed_at = datetime.utcnow()
            error_msg = f"Task execution error: {str(e)}"
            logger.error(f"Task {task_id} failed: {error_msg}", exc_info=True)

            await db.update_status(
                task_id=task_id,
                status="failed",
                completed_at=completed_at,
                error=error_msg
            )

            # Send callback for failure
            task = await db.get_task(task_id)
            if task and task.get("callback_url"):
                await self._send_callback(
                    task_id=task_id,
                    callback_url=task["callback_url"],
                    status="failed",
                    result=None,
                    error=error_msg,
                    completed_at=completed_at
                )

    async def _run_browser_task(
        self,
        task_id: str,
        url: str,
        task_description: str,
        timeout: int
    ) -> str:
        """
        Execute browser automation using browser-use Agent.

        Args:
            task_id: Task UUID for logging
            url: Target URL
            task_description: Natural language task description
            timeout: Timeout in seconds

        Returns:
            str: Result message from the agent

        Raises:
            asyncio.TimeoutError: If task exceeds timeout
            Exception: If browser automation fails
        """
        logger.info(f"Starting browser automation for task {task_id}")
        logger.info(f"URL: {url}")
        logger.info(f"Description: {task_description[:100]}...")

        browser = None
        try:
            # Create Browser instance with CDP connection
            browser = Browser(cdp_url=CHROME_CDP_URL)
            logger.info(f"Connected to Chrome CDP at {CHROME_CDP_URL}")

            # Create Agent with ChatBrowserUse (optimized model)
            agent = Agent(
                task=task_description,
                llm=ChatBrowserUse(),
                browser=browser,
            )

            # Execute task with timeout
            logger.info(f"Executing agent task (timeout: {timeout}s)")
            result = await asyncio.wait_for(
                agent.run(),
                timeout=timeout
            )

            logger.info(f"Agent execution completed for task {task_id}")
            logger.debug(f"Result: {result}")

            # Convert result to string if needed
            if hasattr(result, 'final_result'):
                result_str = str(result.final_result())
            else:
                result_str = str(result)

            return result_str

        except asyncio.TimeoutError:
            logger.warning(f"Browser task {task_id} exceeded timeout of {timeout}s")
            raise

        except Exception as e:
            logger.error(f"Browser task {task_id} failed: {e}", exc_info=True)
            raise

        finally:
            # Clean up browser resources
            # Note: Browser with CDP connection doesn't need explicit cleanup
            # The CDP connection stays open for reuse
            if browser:
                logger.debug(f"Browser task {task_id} cleanup complete")

    async def _send_callback(
        self,
        task_id: str,
        callback_url: str,
        status: str,
        result: Optional[str],
        error: Optional[str],
        completed_at: datetime
    ):
        """
        Send webhook callback to notify about task completion.

        Args:
            task_id: Task UUID
            callback_url: Webhook URL to call
            status: Task status (completed, failed, timeout)
            result: Task result (if successful)
            error: Error message (if failed)
            completed_at: Completion timestamp
        """
        payload = CallbackPayload(
            task_id=task_id,
            status=status,
            result=result,
            error=error,
            completed_at=completed_at
        )

        logger.info(f"Sending callback for task {task_id} to {callback_url}")

        # Retry logic with exponential backoff
        for attempt in range(WEBHOOK_RETRY_ATTEMPTS):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        callback_url,
                        json=payload.model_dump(),
                        timeout=WEBHOOK_TIMEOUT
                    )
                    response.raise_for_status()

                logger.info(f"Callback sent successfully for task {task_id} (attempt {attempt + 1})")
                await db.update_callback_attempt(task_id, attempt + 1, None)
                return

            except Exception as e:
                error_msg = f"Callback attempt {attempt + 1} failed: {str(e)}"
                logger.warning(error_msg)

                # Update database with attempt info
                await db.update_callback_attempt(task_id, attempt + 1, error_msg)

                # Retry with exponential backoff (unless last attempt)
                if attempt < WEBHOOK_RETRY_ATTEMPTS - 1:
                    wait_time = WEBHOOK_RETRY_DELAY * (2 ** attempt)
                    logger.info(f"Retrying callback in {wait_time}s...")
                    await asyncio.sleep(wait_time)

        logger.error(f"All callback attempts failed for task {task_id}")


# Global task queue instance
task_queue = TaskQueue()
