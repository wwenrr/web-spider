"""
Compatibility module for pybgworker app discovery.

The worker app name remains `tasks` so existing scripts keep working.
"""

from infrastructure.jobs.category_crawl_jobs import crawl_category_job
from infrastructure.jobs.product_jobs import crawl_product_url
from infrastructure.jobs.todo_jobs import log_todo_created
from infrastructure.jobs.worker import run_worker

__all__ = ["crawl_category_job", "crawl_product_url", "log_todo_created", "run_worker"]
