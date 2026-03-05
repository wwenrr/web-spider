from nicegui import ui


def render_crawl_form(site: str) -> None:
    with ui.card().classes("card"):
        ui.label("Target Site").classes("field-label")
        ui.label(site).classes("h2")
        ui.label("Supports both /crawl?site=tiki and /crawl?tiki").classes("muted")
