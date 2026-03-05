from typing import Final

ROUTE_ROOT: Final[str] = "/"
ROUTE_DASHBOARD: Final[str] = "/dashboard"
ROUTE_JOB_CREATE: Final[str] = "/jobs/create"
ROUTE_JOB_DETAIL: Final[str] = "/jobs/{todo_id}"
ROUTE_JOB_EDIT: Final[str] = "/jobs/{todo_id}/edit"
ROUTE_CRAWL_PAGE: Final[str] = "/crawl"
ROUTE_CRAWL: Final[str] = "/crawl?site=tiki"


def route_job_detail(todo_id: int) -> str:
    return ROUTE_JOB_DETAIL.format(todo_id=todo_id)


def route_job_edit(todo_id: int) -> str:
    return ROUTE_JOB_EDIT.format(todo_id=todo_id)
