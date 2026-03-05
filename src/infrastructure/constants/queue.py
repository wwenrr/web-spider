from typing import Final

from domain.jobs.constants import AUDIT_EVENT_JOB_CREATED

DEFAULT_WORKER_APP_NAME: Final[str] = "tasks"
TASK_LOG_TODO_CREATED: Final[str] = AUDIT_EVENT_JOB_CREATED

TASK_IMPORT_PATHS: Final[dict[str, str]] = {
    TASK_LOG_TODO_CREATED: "tasks.log_todo_created",
}
