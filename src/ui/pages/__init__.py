from ui.pages.crawl import register_crawl_page
from ui.pages.dashboard import register_dashboard_page
from ui.pages.job_detail import register_job_detail_pages
from ui.pages.jobs import register_jobs_pages

_pages_registered = False


def register_pages() -> None:
    global _pages_registered
    if _pages_registered:
        return

    register_jobs_pages()
    register_dashboard_page()
    register_crawl_page()
    register_job_detail_pages()

    _pages_registered = True
