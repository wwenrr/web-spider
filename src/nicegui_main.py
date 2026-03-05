from nicegui import ui

from domain.jobs.services import JobManager, configure_job_manager
from infrastructure.queues import get_default_job_queue
from infrastructure.repositories.todo import get_job_repository
from ui.constants import FONT, PAGE_TITLE, build_favicon_head_html
from ui.pages import register_pages
from ui.static import build_css


def run_app() -> None:
    configure_job_manager(
        JobManager(
            repository=get_job_repository(),
            queue=get_default_job_queue(),
        )
    )
    register_pages()

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
