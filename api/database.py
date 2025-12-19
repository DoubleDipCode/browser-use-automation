"""
Database operations for task storage using SQLite with WAL mode.
"""
import json
import aiosqlite
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from api.config import DATABASE_PATH


class TaskDatabase:
    """Manages SQLite database operations for tasks."""

    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize database with schema and enable WAL mode."""
        async with aiosqlite.connect(self.db_path) as db:
            # Enable WAL mode for concurrent access
            await db.execute("PRAGMA journal_mode=WAL")

            # Create tasks table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    url TEXT NOT NULL,
                    task_description TEXT NOT NULL,
                    form_data TEXT,
                    callback_url TEXT,
                    timeout INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    result TEXT,
                    error TEXT,
                    callback_attempts INTEGER DEFAULT 0,
                    last_callback_error TEXT,
                    created_at TIMESTAMP NOT NULL,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP
                )
            """)

            # Create index on status for faster queries
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_tasks_status
                ON tasks(status)
            """)

            # Create index on created_at for sorting
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_tasks_created_at
                ON tasks(created_at DESC)
            """)

            await db.commit()

    async def mark_incomplete_as_failed(self):
        """
        Mark all queued or running tasks as failed on server startup.
        This prevents orphaned tasks from appearing stuck forever.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE tasks
                SET status = 'failed',
                    error = 'Server restarted during execution',
                    completed_at = ?
                WHERE status IN ('queued', 'running')
            """, (datetime.utcnow().isoformat(),))
            await db.commit()

    async def create_task(
        self,
        task_id: str,
        url: str,
        task_description: str,
        form_data: Dict[str, Any],
        callback_url: Optional[str],
        timeout: int
    ) -> Dict[str, Any]:
        """Create a new task in the database."""
        now = datetime.utcnow()

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO tasks (
                    task_id, url, task_description, form_data,
                    callback_url, timeout, status, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, 'queued', ?)
            """, (
                task_id,
                url,
                task_description,
                json.dumps(form_data),
                callback_url,
                timeout,
                now.isoformat()
            ))
            await db.commit()

        return {
            "task_id": task_id,
            "status": "queued",
            "created_at": now
        }

    async def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a task by ID."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM tasks WHERE task_id = ?",
                (task_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return dict(row)
                return None

    async def list_tasks(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> tuple[List[Dict[str, Any]], int]:
        """
        List tasks with optional filtering and pagination.
        Returns (tasks, total_count).
        """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            # Build query based on filter
            if status:
                query = "SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC LIMIT ? OFFSET ?"
                count_query = "SELECT COUNT(*) FROM tasks WHERE status = ?"
                params = (status, limit, offset)
                count_params = (status,)
            else:
                query = "SELECT * FROM tasks ORDER BY created_at DESC LIMIT ? OFFSET ?"
                count_query = "SELECT COUNT(*) FROM tasks"
                params = (limit, offset)
                count_params = ()

            # Get tasks
            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                tasks = [dict(row) for row in rows]

            # Get total count
            async with db.execute(count_query, count_params) as cursor:
                total = (await cursor.fetchone())[0]

            return tasks, total

    async def update_status(
        self,
        task_id: str,
        status: str,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        result: Optional[str] = None,
        error: Optional[str] = None
    ):
        """Update task status and related fields."""
        async with aiosqlite.connect(self.db_path) as db:
            updates = ["status = ?"]
            params = [status]

            if started_at:
                updates.append("started_at = ?")
                params.append(started_at.isoformat())

            if completed_at:
                updates.append("completed_at = ?")
                params.append(completed_at.isoformat())

            if result is not None:
                updates.append("result = ?")
                params.append(result)

            if error is not None:
                updates.append("error = ?")
                params.append(error)

            params.append(task_id)

            await db.execute(
                f"UPDATE tasks SET {', '.join(updates)} WHERE task_id = ?",
                params
            )
            await db.commit()

    async def update_callback_attempt(
        self,
        task_id: str,
        attempts: int,
        error: Optional[str] = None
    ):
        """Update callback attempt count and error."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE tasks
                SET callback_attempts = ?,
                    last_callback_error = ?
                WHERE task_id = ?
            """, (attempts, error, task_id))
            await db.commit()

    async def delete_task(self, task_id: str) -> bool:
        """
        Delete a task from the database.
        Returns True if task was deleted, False if not found.
        """
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "DELETE FROM tasks WHERE task_id = ?",
                (task_id,)
            )
            await db.commit()
            return cursor.rowcount > 0


# Singleton instance
db = TaskDatabase()


async def init_database():
    """Initialize database (called on application startup)."""
    await db.initialize()
    await db.mark_incomplete_as_failed()


# For running as a script to initialize the database
if __name__ == "__main__":
    import asyncio

    async def main():
        print(f"Initializing database at {DATABASE_PATH}")
        await db.initialize()
        print("Database initialized successfully")
        print(f"WAL mode enabled: Check {DATABASE_PATH}-wal file will be created on first write")

        # Verify WAL mode
        async with aiosqlite.connect(DATABASE_PATH) as conn:
            async with conn.execute("PRAGMA journal_mode") as cursor:
                mode = await cursor.fetchone()
                print(f"Journal mode: {mode[0]}")

    asyncio.run(main())
