from pathlib import Path

from nicegui import app, ui

from core.cdp_connections.facade import configure_cdp_connection_manager
from core.cdp_connections.services import CdpConnectionManager
from core.monitoring.facade import configure_queue_monitoring_manager
from core.monitoring.services import QueueMonitoringManager
from core.products.facade import configure_product_manager
from core.products.services import ProductManager
from core.todos.facade import configure_todo_manager
from core.todos.services import TodoManager
from infrastructure.queues import get_default_job_queue
from infrastructure.repositories.cdp_connection import get_cdp_connection_repository
from infrastructure.repositories.product import get_product_repository
from infrastructure.repositories.queue_monitoring import get_queue_monitoring_repository
from infrastructure.repositories.todo import get_todo_repository
from ui.constants import FONT, PAGE_TITLE, build_favicon_head_html
from ui.pages import register_pages
from ui.static import build_css


def run_app() -> None:
    configure_cdp_connection_manager(
        CdpConnectionManager(
            repository=get_cdp_connection_repository(),
        )
    )
    configure_todo_manager(
        TodoManager(
            repository=get_todo_repository(),
            task_queue=get_default_job_queue(),
        )
    )
    configure_product_manager(
        ProductManager(
            repository=get_product_repository(),
            task_queue=get_default_job_queue(),
        )
    )
    configure_queue_monitoring_manager(
        QueueMonitoringManager(
            repository=get_queue_monitoring_repository(),
        )
    )
    register_pages()
    app.add_static_files("/static", str(Path(__file__).resolve().parent / "ui" / "static"))

    ui.add_head_html(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        f'<link href="https://fonts.googleapis.com/css2?family={FONT}:wght@400;500;600;700&display=swap" rel="stylesheet">'
        f"{build_favicon_head_html()}",
        shared=True,
    )
    ui.add_css(build_css(), shared=True)
    ui.run(host="0.0.0.0", port=3000, title=PAGE_TITLE, show=False, reload=True)


if __name__ in {"__main__", "__mp_main__"}:
    run_app()
