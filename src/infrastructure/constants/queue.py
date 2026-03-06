from typing import Final

from core.category_crawls.constants import CRAWL_EVENT_CATEGORY_JOB
from core.products.constants import CRAWL_EVENT_PRODUCT_URL
from core.todos.constants import AUDIT_EVENT_JOB_CREATED

DEFAULT_WORKER_APP_NAME: Final[str] = "tasks"
TASK_LOG_TODO_CREATED: Final[str] = AUDIT_EVENT_JOB_CREATED
TASK_CRAWL_CATEGORY_JOB: Final[str] = CRAWL_EVENT_CATEGORY_JOB
TASK_CRAWL_PRODUCT_URL: Final[str] = CRAWL_EVENT_PRODUCT_URL

TASK_IMPORT_PATHS: Final[dict[str, str]] = {
    TASK_LOG_TODO_CREATED: "infrastructure.jobs.todo_jobs.log_todo_created",
    TASK_CRAWL_CATEGORY_JOB: "infrastructure.jobs.category_crawl_jobs.crawl_category_job",
    TASK_CRAWL_PRODUCT_URL: "infrastructure.jobs.product_jobs.crawl_product_url",
}
