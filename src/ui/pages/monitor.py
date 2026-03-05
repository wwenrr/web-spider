from collections.abc import Iterable
from datetime import datetime

from nicegui import ui

from infrastructure.queues.monitoring import QueueJob, QueueStats, get_queue_stats, list_queue_jobs
from ui.constants import PAGE_TITLE, ROUTE_MONITOR
from ui.layout import build_page


def register_monitor_page() -> None:
    @ui.page(ROUTE_MONITOR)
    def monitor_jobs_page() -> None:
        ui.page_title(PAGE_TITLE)
        body = build_page(
            page="monitor",
            title="Job Monitor",
            subtitle="Monitor queue jobs and worker operations in one place.",
        )
        with body:
            stats = get_queue_stats()
            queue_jobs = list_queue_jobs(limit=30)
            _render_monitor_overview(stats)
            _render_monitor_jobs(queue_jobs)
            _render_pybgworker_cli()
            _render_observability_notes()


def _render_monitor_overview(stats: QueueStats) -> None:
    with ui.element("div").classes("monitor-metrics"):
        _render_metric_card("Total Jobs", str(stats.total), "Current records from pybgworker.tasks.")
        _render_metric_card("Pending", str(stats.pending), "Queued and waiting to run.")
        _render_metric_card("Running", str(stats.running), "Jobs currently being processed.")
        _render_metric_card("Failed", str(stats.failed), "Jobs that ended with error/cancel.")


def _render_monitor_jobs(queue_jobs: list[QueueJob]) -> None:
    with ui.card().classes("card monitor-card").style("align-items: stretch;"):
        ui.label("Recent Jobs").classes("field-label")
        if not queue_jobs:
            ui.label("No queue jobs found in pybgworker DB.").classes("todo-empty")
            return

        with ui.column().classes("monitor-job-list full-width").style("width: 100%; align-self: stretch;"):
            for queue_job in queue_jobs:
                _render_job_row(queue_job)


def _render_pybgworker_cli() -> None:
    with ui.card().classes("card monitor-card"):
        ui.label("pybgworker CLI").classes("field-label")
        ui.label("Use these commands to inspect and operate worker queues.").classes("muted monitor-note")
        _render_command_list(
            [
                "python -m pybgworker.cli inspect",
                "python -m pybgworker.cli stats",
                "python -m pybgworker.cli failed",
                "python -m pybgworker.cli retry <task_id>",
                "python -m pybgworker.cli cancel <task_id>",
                "python -m pybgworker.cli purge",
            ]
        )


def _render_observability_notes() -> None:
    with ui.card().classes("card monitor-card"):
        ui.label("Observability Notes").classes("field-label")
        ui.label("Enable JSON logs for task start, success, failure, duration, and heartbeat events.").classes(
            "muted monitor-note"
        )
        ui.label("Pipe logs into ELK, Prometheus stack, or custom alerting for dashboards.").classes(
            "muted monitor-note"
        )

        ui.label("SQLite Quick Query").classes("field-label monitor-subhead")
        _render_command_list(
            [
                "SELECT * FROM tasks WHERE status = 'pending';",
                "SELECT * FROM results ORDER BY created_at DESC LIMIT 20;",
            ]
        )
        ui.label("Use --retention-days 30 to keep DB size under control.").classes("muted monitor-note")


def _render_metric_card(title: str, value: str, detail: str) -> None:
    with ui.element("div").classes("monitor-metric-card"):
        ui.label(title).classes("monitor-metric-title")
        ui.label(value).classes("monitor-metric-value")
        ui.label(detail).classes("monitor-metric-detail")


def _render_job_row(queue_job: QueueJob) -> None:
    status = queue_job.status.upper()
    with ui.element("div").classes("monitor-job-row full-width").style("width: 100%;"):
        with ui.column().classes("gap-0"):
            ui.label(queue_job.name).classes("todo-title")
            ui.label(f"Task {queue_job.id} • Attempt {queue_job.attempt}/{queue_job.max_retries}").classes("todo-id")
        ui.label(status).classes(_chip_class_for_status(queue_job.status))
        ui.label(_format_job_time(queue_job.updated_at or queue_job.created_at)).classes("monitor-job-time")


def _format_job_time(raw_time: object) -> str:
    if isinstance(raw_time, datetime):
        return raw_time.strftime("%Y-%m-%d %H:%M:%S UTC")

    if isinstance(raw_time, str):
        normalized = raw_time.strip()
        if not normalized:
            return "Unknown update time"

        parsed = _parse_iso_datetime(normalized)
        if parsed is not None:
            return parsed.strftime("%Y-%m-%d %H:%M:%S UTC")

        return normalized

    return "Unknown update time"


def _parse_iso_datetime(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _chip_class_for_status(status: str) -> str:
    normalized = status.lower()
    if normalized in {"success", "done", "completed"}:
        return "chip chip--green"
    if normalized in {"failed", "error", "cancelled", "canceled", "dead"}:
        return "chip chip--red"
    if normalized in {"running", "processing", "in_progress", "locked"}:
        return "chip chip--blue"
    return "chip chip--amber"


def _render_command_list(commands: Iterable[str]) -> None:
    with ui.column().classes("monitor-command-list"):
        for command in commands:
            ui.label(command).classes("monitor-command")
