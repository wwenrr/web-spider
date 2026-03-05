from nicegui import ui


def render_status_badge(is_done: bool) -> None:
    if is_done:
        ui.label("Done").classes("chip chip--green tc")
        return
    ui.label("Pending").classes("chip chip--amber tc")
