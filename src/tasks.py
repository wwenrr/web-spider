"""
Compatibility module for pybgworker app discovery.

The worker app name remains `tasks` so existing scripts keep working.
"""

from infrastructure.jobs.todo_jobs import log_todo_created
from infrastructure.jobs.worker import run_worker

__all__ = ["log_todo_created", "run_worker"]
