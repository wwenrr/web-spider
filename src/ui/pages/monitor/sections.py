from collections.abc import Callable

from nicegui import ui

from core.monitoring.facade import get_queue_stats, list_queue_jobs
from core.monitoring.models import QueueJob, QueueStats
from ui.pages.monitor.components import render_command_list, render_job_row, render_metric_card

_refresh_callback: Callable[[], None] | None = None


def render_monitor_live_sections() -> None:
    @ui.refreshable
    def render_live_metrics() -> None:
        _render_monitor_overview(get_queue_stats())

    @ui.refreshable
    def render_live_jobs() -> None:
        _render_monitor_jobs(list_queue_jobs(limit=30))

    render_live_metrics()
    render_live_jobs()
    global _refresh_callback
    _refresh_callback = lambda: (render_live_metrics.refresh(), render_live_jobs.refresh())


def refresh_monitor_live_sections() -> None:
    if _refresh_callback is not None:
        _refresh_callback()


def render_pybgworker_cli() -> None:
    with ui.card().classes("card monitor-card"):
        ui.label("pybgworker CLI").classes("field-label")
        ui.label("Use these commands to inspect and operate worker queues.").classes("muted monitor-note")
        render_command_list(
            [
                "python -m pybgworker.cli inspect",
                "python -m pybgworker.cli stats",
                "python -m pybgworker.cli failed",
                "python -m pybgworker.cli retry <task_id>",
                "python -m pybgworker.cli cancel <task_id>",
                "python -m pybgworker.cli purge",
            ]
        )


def render_observability_notes() -> None:
    with ui.card().classes("card monitor-card"):
        ui.label("Observability Notes").classes("field-label")
        ui.label("Enable JSON logs for task start, success, failure, duration, and heartbeat events.").classes(
            "muted monitor-note"
        )
        ui.label("Pipe logs into ELK, Prometheus stack, or custom alerting for dashboards.").classes(
            "muted monitor-note"
        )

        ui.label("SQLite Quick Query").classes("field-label monitor-subhead")
        render_command_list(
            [
                "SELECT * FROM tasks WHERE status = 'pending';",
                "SELECT * FROM results ORDER BY created_at DESC LIMIT 20;",
            ]
        )
        ui.label("Use --retention-days 30 to keep DB size under control.").classes("muted monitor-note")


def _render_monitor_overview(stats: QueueStats) -> None:
    with ui.element("div").classes("monitor-metrics"):
        render_metric_card("Total Jobs", str(stats.total), "Current records from pybgworker.tasks.")
        render_metric_card("Pending", str(stats.pending), "Queued and waiting to run.")
        render_metric_card("Running", str(stats.running), "Jobs currently being processed.")
        render_metric_card("Failed", str(stats.failed), "Jobs that ended with error/cancel.")


def _render_monitor_jobs(queue_jobs: list[QueueJob]) -> None:
    with ui.card().classes("card monitor-card"):
        ui.label("Recent Jobs").classes("field-label")
        if not queue_jobs:
            ui.label("No queue jobs found in pybgworker DB.").classes("todo-empty")
            return

        with ui.element("div").classes("monitor-job-list"):
            for queue_job in queue_jobs:
                render_job_row(queue_job)
