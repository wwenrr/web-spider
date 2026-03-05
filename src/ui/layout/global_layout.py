from nicegui import ui

from ui.constants import ROUTE_CRAWL, ROUTE_DASHBOARD, ROUTE_JOB_CREATE, SIDEBAR_LOGO_HTML


def build_shell(page: str, title: str, subtitle: str) -> ui.column:
    with ui.element("div").classes("shell"):
        _render_sidebar(page)
        with ui.element("div").classes("content"):
            with ui.element("div").classes("content-inner"):
                with ui.row().classes("page-hdr"):
                    with ui.column().classes("gap-0"):
                        ui.label(title).classes("page-title")
                        ui.label(subtitle).classes("page-sub")
                body = ui.column().classes("page-body")
    return body


def _render_sidebar(page: str) -> None:
    with ui.element("nav").classes("nav"):
        with ui.element("div").classes("nav-head"):
            ui.html(
                f'<div class="nav-logo">{SIDEBAR_LOGO_HTML}</div>',
                sanitize=False,
            )
            with ui.column().classes("gap-0 nav-brand"):
                ui.label("Web Spider").classes("nav-brand-title")
                ui.label("Automation Console").classes("nav-brand-sub")

        _render_link("Dashboard", "dashboard", ROUTE_DASHBOARD, page == "dashboard")

        ui.label("OPERATIONS").classes("nav-section")
        _render_link("AI API Token", "key", ROUTE_JOB_CREATE, page == "create")
        _render_link("Crawl Settings", "webhook", ROUTE_CRAWL, page == "crawl")

        ui.label("INTEGRATIONS").classes("nav-section")
        _render_link("WordPress", "language", ROUTE_DASHBOARD, False, disabled=True)
        _render_link("Discord", "forum", ROUTE_DASHBOARD, False, disabled=True)

        ui.element("div").classes("nav-grow")


def _render_link(label: str, icon: str, href: str, active: bool, disabled: bool = False) -> None:
    cls = "nav-item nav-item--on" if active else "nav-item"
    if disabled:
        with ui.element("div").classes(f"{cls} nav-item--disabled"):
            with ui.element("span").classes("nav-item-ic-wrap"):
                ui.icon(icon).classes("nav-item-ic")
            ui.label(label).classes("nav-item-lbl")
            ui.label("Soon").classes("nav-item-tag")
        return

    with ui.link(target=href).classes(cls):
        with ui.element("span").classes("nav-item-ic-wrap"):
            ui.icon(icon).classes("nav-item-ic")
        ui.label(label).classes("nav-item-lbl")
