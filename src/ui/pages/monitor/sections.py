from collections.abc import Callable

from nicegui import ui

from core.monitoring.facade import count_queue_jobs, get_queue_stats, list_queue_jobs
from core.monitoring.models import QueueJob, QueueStats
from ui.pages.monitor.components import render_command_list, render_job_row, render_metric_card

MONITOR_PAGE_SIZE = 20
MONITOR_STATUS_FILTERS: tuple[tuple[str, str | None], ...] = (
    ("All", None),
    ("Pending", "pending"),
    ("Running", "running"),
    ("Done", "done"),
    ("Failed", "failed"),
)
_refresh_callback: Callable[[], None] | None = None


def render_monitor_live_sections() -> None:
    state: dict[str, object] = {
        "page": 1,
        "status_filter": None,
    }

    @ui.refreshable
    def render_live_metrics() -> None:
        _render_monitor_overview(get_queue_stats())

    @ui.refreshable
    def render_live_jobs() -> None:
        page = _state_page(state)
        status_filter = _state_status_filter(state)
        total_jobs = count_queue_jobs(status_filter=status_filter)
        total_pages = max(1, (total_jobs + MONITOR_PAGE_SIZE - 1) // MONITOR_PAGE_SIZE)
        current_page = min(page, total_pages)
        if current_page != page:
            state["page"] = current_page
        offset = (current_page - 1) * MONITOR_PAGE_SIZE
        queue_jobs = list_queue_jobs(limit=MONITOR_PAGE_SIZE, offset=offset, status_filter=status_filter)
        _render_monitor_jobs(
            queue_jobs=queue_jobs,
            active_status=status_filter,
            total_jobs=total_jobs,
            current_page=current_page,
            total_pages=total_pages,
            on_select_status=lambda next_status: _set_monitor_status_filter(next_status, state, render_live_jobs.refresh),
            on_previous=lambda: _change_monitor_page(-1, state, total_pages, render_live_jobs.refresh),
            on_next=lambda: _change_monitor_page(1, state, total_pages, render_live_jobs.refresh),
        )

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


def _render_monitor_jobs(
    queue_jobs: list[QueueJob],
    active_status: str | None,
    total_jobs: int,
    current_page: int,
    total_pages: int,
    on_select_status: Callable[[str | None], None],
    on_previous: Callable[[], None],
    on_next: Callable[[], None],
) -> None:
    with ui.card().classes("card monitor-card"):
        ui.label("Recent Jobs").classes("field-label")
        _render_monitor_toolbar(
            active_status=active_status,
            total_jobs=total_jobs,
            current_page=current_page,
            total_pages=total_pages,
            on_select_status=on_select_status,
            on_previous=on_previous,
            on_next=on_next,
        )
        if not queue_jobs:
            ui.label("No queue jobs found in pybgworker DB.").classes("todo-empty")
            return

        with ui.element("div").classes("monitor-job-list"):
            for queue_job in queue_jobs:
                render_job_row(queue_job)


def _render_monitor_toolbar(
    active_status: str | None,
    total_jobs: int,
    current_page: int,
    total_pages: int,
    on_select_status: Callable[[str | None], None],
    on_previous: Callable[[], None],
    on_next: Callable[[], None],
) -> None:
    with ui.element("div").classes("monitor-toolbar"):
        with ui.element("div").classes("monitor-toolbar-group"):
            ui.label("Status").classes("monitor-toolbar-kicker")
            with ui.element("div").classes("monitor-filter-row"):
                for label, value in MONITOR_STATUS_FILTERS:
                    classes = "monitor-filter monitor-filter--active" if value == active_status else "monitor-filter"
                    with ui.element("button").classes(classes).props("type=button").on(
                        "click",
                        lambda _event=None, next_status=value: on_select_status(next_status),
                    ):
                        ui.label(label).classes("monitor-filter-label")

        with ui.element("div").classes("monitor-toolbar-group monitor-toolbar-group--meta"):
            ui.label(f"{total_jobs} items").classes("monitor-pagination-copy")
            with ui.element("div").classes("monitor-pagination"):
                previous_props = "type=button disabled" if current_page <= 1 else "type=button"
                next_props = "type=button disabled" if current_page >= total_pages else "type=button"
                previous_button = ui.element("button").classes("monitor-page-btn").props(previous_props)
                if current_page > 1:
                    previous_button.on("click", lambda _event=None: on_previous())
                with previous_button:
                    ui.label("Prev").classes("monitor-page-btn-label")
                ui.label(f"Page {current_page} / {total_pages}").classes("monitor-page-indicator")
                next_button = ui.element("button").classes("monitor-page-btn").props(next_props)
                if current_page < total_pages:
                    next_button.on("click", lambda _event=None: on_next())
                with next_button:
                    ui.label("Next").classes("monitor-page-btn-label")


def _change_monitor_page(
    step: int,
    state: dict[str, object],
    total_pages: int,
    refresh_live_jobs: Callable[[], None],
) -> None:
    current_page = _state_page(state)
    next_page = max(1, min(current_page + step, total_pages))
    if next_page == current_page:
        return
    state["page"] = next_page
    refresh_live_jobs()


def _set_monitor_status_filter(
    next_status: str | None,
    state: dict[str, object],
    refresh_live_jobs: Callable[[], None],
) -> None:
    if _state_status_filter(state) == next_status:
        return
    state["status_filter"] = next_status
    state["page"] = 1
    refresh_live_jobs()


def _state_page(state: dict[str, object]) -> int:
    raw_page = state.get("page")
    if not isinstance(raw_page, int):
        return 1
    return max(1, raw_page)


def _state_status_filter(state: dict[str, object]) -> str | None:
    raw_status = state.get("status_filter")
    if not isinstance(raw_status, str):
        return None
    normalized_status = raw_status.strip()
    if normalized_status == "":
        return None
    return normalized_status
