from ui.pages.dashboard import register_dashboard_page
from ui.pages.todos import register_todos_page

_pages_registered = False


def register_pages() -> None:
    global _pages_registered
    if _pages_registered:
        return

    register_dashboard_page()
    register_todos_page()

    _pages_registered = True
