from ui.pages.app.index import register_app_page

_pages_registered = False


def register_pages() -> None:
    global _pages_registered
    if _pages_registered:
        return

    register_app_page()

    _pages_registered = True
