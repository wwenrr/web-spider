from collections.abc import Iterable

from nicegui import ui

from core.monitoring.models import QueueJob
from ui.pages.monitor.formatters import chip_class_for_status, format_job_time


def render_metric_card(title: str, value: str, detail: str) -> None:
    with ui.element("div").classes("monitor-metric-card"):
        ui.label(title).classes("monitor-metric-title")
        ui.label(value).classes("monitor-metric-value")
        ui.label(detail).classes("monitor-metric-detail")


def render_job_row(queue_job: QueueJob) -> None:
    status = queue_job.status.upper()
    with ui.element("div").classes("monitor-job-row"):
        with ui.element("div").classes("monitor-job-info"):
            ui.label(queue_job.name).classes("todo-title")
            ui.label(f"Task {queue_job.id} • Attempt {queue_job.attempt}/{queue_job.max_retries}").classes("todo-id")
        ui.label(status).classes(chip_class_for_status(queue_job.status))
        ui.label(format_job_time(queue_job.updated_at or queue_job.created_at)).classes("monitor-job-time")


def render_command_list(commands: Iterable[str]) -> None:
    with ui.element("div").classes("monitor-command-list"):
        for command in commands:
            ui.label(command).classes("monitor-command")
