from collections.abc import Callable
from datetime import datetime
from html import escape
import json
from typing import Final

from nicegui import ui

from core.products.facade import delete_product, enqueue_product_url, list_products
from infrastructure.models.product import Product
from ui.helpers import show_error, show_success

PRODUCT_URL_INPUT_ID: Final[str] = "spy-products-url-input"
_refresh_callback: Callable[[], None] | None = None


def render_products_crawl_section() -> None:
    state: dict[str, object] = {
        "gallery_images": [],
        "gallery_title": "",
        "gallery_index": 0,
    }

    with ui.element("section").classes("spy-products-card"):
        _render_text("h3", "Products Crawl Queue", "spy-products-title")
        _render_text(
            "p",
            "Enter a product page URL to create a pending record. The worker will process it in the background after 10 seconds.",
            "spy-products-note muted",
        )

        @ui.refreshable
        def render_products_index() -> None:
            products = list_products(limit=50)
            if not products:
                _render_text("span", "No products in the crawl queue yet.", "todo-empty")
                return
            _render_products_table(
                products,
                on_delete=lambda product_id: _delete_product(product_id, render_products_index.refresh),
                on_view_images=lambda title, images: _open_gallery(title, images, state, render_gallery.refresh),
            )

        @ui.refreshable
        def render_gallery() -> None:
            _render_gallery_modal(
                state,
                on_close=lambda: _close_gallery(state, render_gallery.refresh),
                on_select=lambda image_index: _select_gallery_image(image_index, state, render_gallery.refresh),
                on_previous=lambda: _step_gallery(-1, state, render_gallery.refresh),
                on_next=lambda: _step_gallery(1, state, render_gallery.refresh),
            )

        async def _handle_submit(_event: object | None = None) -> None:
            await _submit_product_url(render_products_index.refresh)

        with ui.element("form").classes("spy-products-form-row").on("submit.prevent", _handle_submit):
            ui.html(
                f'<input id="{PRODUCT_URL_INPUT_ID}" class="spy-products-input" '
                'type="url" placeholder="https://www.1999.co.jp/..." autocomplete="off">'
            )
            with ui.element("button").classes("spy-products-submit").props("type=submit"):
                _render_text("span", "Queue Crawl", "spy-products-submit-label")

        render_products_index()
        render_gallery()
        global _refresh_callback
        _refresh_callback = render_products_index.refresh


def refresh_products_crawl_section() -> None:
    if _refresh_callback is not None:
        _refresh_callback()


async def _submit_product_url(refresh_index: Callable[[], None]) -> None:
    raw_remote_url = await _read_product_url_input()
    remote_url = raw_remote_url.strip()
    if remote_url == "":
        show_error("Please enter a product URL.")
        return

    try:
        enqueue_product_url(remote_url)
    except ValueError as err:
        show_error(str(err))
        return

    await _clear_product_url_input()
    refresh_index()
    show_success("Product queued as pending.")


def _render_products_table(
    products: list[Product],
    on_delete: Callable[[int], None],
    on_view_images: Callable[[str, list[str]], None],
) -> None:
    with ui.element("div").classes("spy-products-table-wrap"):
        with ui.element("table").classes("spy-products-table"):
            with ui.element("thead"):
                with ui.element("tr"):
                    _render_text("th", "Thumbnail", "spy-products-th")
                    _render_text("th", "Name", "spy-products-th")
                    _render_text("th", "Price", "spy-products-th")
                    _render_text("th", "Code", "spy-products-th")
                    _render_text("th", "Barcode", "spy-products-th")
                    _render_text("th", "Remote URL", "spy-products-th")
                    _render_text("th", "Status", "spy-products-th")
                    _render_text("th", "Category", "spy-products-th")
                    _render_text("th", "Crawl At", "spy-products-th")
                    _render_text("th", "Actions", "spy-products-th")

            with ui.element("tbody"):
                for product in products:
                    _render_product_row(product, on_delete, on_view_images)


def _render_product_row(
    product: Product,
    on_delete: Callable[[int], None],
    on_view_images: Callable[[str, list[str]], None],
) -> None:
    categories = _parse_string_array(product.category)
    images = _parse_string_array(product.images_url)
    gallery_images = images if images else ([product.thumbnail] if product.thumbnail else [])
    gallery_title = product.name or product.remote_url

    with ui.element("tr"):
        with ui.element("td").classes("spy-products-td spy-products-td-thumb-cell"):
            if product.thumbnail:
                with ui.element("button").classes("spy-products-thumb-btn").props("type=button").on(
                    "click",
                    lambda _event=None, title=gallery_title, image_urls=gallery_images: on_view_images(title, image_urls),
                ):
                    ui.html(
                        f'<img class="spy-products-thumb" src="{escape(product.thumbnail)}" alt="{escape(gallery_title)} thumbnail">'
                    )
            else:
                _render_text("span", "-", "spy-products-thumb-empty")
        _render_text("td", product.name or "-", "spy-products-td")
        _render_text("td", product.price or "-", "spy-products-td spy-products-td--mono")
        _render_text("td", product.code or "-", "spy-products-td spy-products-td--mono")
        _render_text("td", product.barcode or "-", "spy-products-td spy-products-td--mono")
        with ui.element("td").classes("spy-products-td"):
            with ui.element("a").classes("spy-products-url").props(
                f'href="{escape(product.remote_url)}" target="_blank" rel="noreferrer noopener"'
            ):
                _render_text("span", product.remote_url, "spy-products-url-label")
        _render_text("td", product.crawl_status, f"spy-products-td spy-products-status spy-products-status--{product.crawl_status}")
        with ui.element("td").classes("spy-products-td"):
            if categories:
                with ui.element("ul").classes("spy-products-category-list"):
                    for category in categories:
                        with ui.element("li").classes("spy-products-category-item"):
                            _render_text("span", category, "spy-products-category-text")
            else:
                _render_text("span", "-", "spy-products-category-empty")
        _render_text("td", _format_time(product.crawl_at), "spy-products-td spy-products-td--mono")
        with ui.element("td").classes("spy-products-td spy-products-td-actions"):
            with ui.element("div").classes("spy-products-actions"):
                if gallery_images:
                    with ui.element("button").classes("spy-products-view").props("type=button").on(
                        "click",
                        lambda _event=None, title=gallery_title, image_urls=gallery_images: on_view_images(
                            title,
                            image_urls,
                        ),
                    ):
                        with ui.element("span").classes("spy-products-view-copy"):
                            _render_text("span", "View", "spy-products-view-label")
                            _render_text("sup", str(len(gallery_images)), "spy-products-view-count")
                with ui.element("button").classes("spy-products-delete").props("type=button").on(
                    "click",
                    lambda _event=None, product_id=product.id: on_delete(product_id),
                ):
                    _render_text("span", "Delete", "spy-products-delete-label")


def _delete_product(product_id: int, refresh_index: Callable[[], None]) -> None:
    deleted = delete_product(product_id)
    if not deleted:
        show_error("Product no longer exists.")
        refresh_index()
        return

    refresh_index()
    show_success("Product deleted.")


def _render_gallery_modal(
    state: dict[str, object],
    on_close: Callable[[], None],
    on_select: Callable[[int], None],
    on_previous: Callable[[], None],
    on_next: Callable[[], None],
) -> None:
    images = _gallery_images(state)
    if not images:
        return

    active_index = _gallery_index(state, len(images))
    active_image = images[active_index]
    title = str(state.get("gallery_title") or "Product Images")

    with ui.element("div").classes("spy-gallery-overlay").on("click", lambda _event=None: on_close()):
        with ui.element("div").classes("spy-gallery-modal").on("click.stop"):
            with ui.element("div").classes("spy-gallery-head"):
                with ui.element("div").classes("spy-gallery-head-copy"):
                    _render_text("span", "Product Gallery", "spy-gallery-kicker")
                    _render_text("h4", title, "spy-gallery-title")
                with ui.element("button").classes("spy-gallery-close").props("type=button").on(
                    "click",
                    lambda _event=None: on_close(),
                ):
                    _render_text("span", "x", "spy-gallery-close-label")

            with ui.element("div").classes("spy-gallery-stage"):
                with ui.element("button").classes("spy-gallery-nav").props("type=button").on(
                    "click",
                    lambda _event=None: on_previous(),
                ):
                    _render_text("span", "<", "spy-gallery-nav-label")
                with ui.element("div").classes("spy-gallery-canvas"):
                    ui.html(f'<img class="spy-gallery-image" src="{escape(active_image)}" alt="{escape(title)}">')
                with ui.element("button").classes("spy-gallery-nav").props("type=button").on(
                    "click",
                    lambda _event=None: on_next(),
                ):
                    _render_text("span", ">", "spy-gallery-nav-label")

            with ui.element("div").classes("spy-gallery-meta"):
                _render_text("span", f"Image {active_index + 1} of {len(images)}", "spy-gallery-count")

            with ui.element("div").classes("spy-gallery-strip"):
                for image_index, image_url in enumerate(images):
                    button_classes = "spy-gallery-thumb spy-gallery-thumb--active" if image_index == active_index else "spy-gallery-thumb"
                    with ui.element("button").classes(button_classes).props("type=button").on(
                        "click",
                        lambda _event=None, target_index=image_index: on_select(target_index),
                    ):
                        ui.html(
                            f'<img class="spy-gallery-thumb-image" src="{escape(image_url)}" alt="{escape(title)} thumbnail {image_index + 1}">'
                        )


def _parse_string_array(raw_value: object) -> list[str]:
    if not isinstance(raw_value, str):
        return []
    try:
        payload = json.loads(raw_value)
    except json.JSONDecodeError:
        return []
    if not isinstance(payload, list):
        return []
    return [str(item).strip() for item in payload if str(item).strip() != ""]


def _format_time(raw_time: object) -> str:
    if isinstance(raw_time, datetime):
        return raw_time.strftime("%d/%m/%Y %H:%M:%S")
    normalized = str(raw_time or "").strip()
    if normalized == "":
        return "-"
    try:
        parsed = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError:
        return normalized
    return parsed.strftime("%d/%m/%Y %H:%M:%S")


def _open_gallery(
    title: str,
    images: list[str],
    state: dict[str, object],
    refresh_gallery: Callable[[], None],
) -> None:
    state["gallery_title"] = title
    state["gallery_images"] = images
    state["gallery_index"] = 0
    refresh_gallery()


def _close_gallery(state: dict[str, object], refresh_gallery: Callable[[], None]) -> None:
    state["gallery_title"] = ""
    state["gallery_images"] = []
    state["gallery_index"] = 0
    refresh_gallery()


def _select_gallery_image(
    image_index: int,
    state: dict[str, object],
    refresh_gallery: Callable[[], None],
) -> None:
    images = _gallery_images(state)
    if not images:
        return
    state["gallery_index"] = max(0, min(image_index, len(images) - 1))
    refresh_gallery()


def _step_gallery(
    step: int,
    state: dict[str, object],
    refresh_gallery: Callable[[], None],
) -> None:
    images = _gallery_images(state)
    if not images:
        return
    current_index = _gallery_index(state, len(images))
    state["gallery_index"] = (current_index + step) % len(images)
    refresh_gallery()


def _gallery_images(state: dict[str, object]) -> list[str]:
    raw_images = state.get("gallery_images")
    if not isinstance(raw_images, list):
        return []
    return [str(item).strip() for item in raw_images if str(item).strip() != ""]


def _gallery_index(state: dict[str, object], images_count: int) -> int:
    raw_index = state.get("gallery_index")
    if not isinstance(raw_index, int):
        return 0
    if images_count <= 0:
        return 0
    return max(0, min(raw_index, images_count - 1))


async def _read_product_url_input() -> str:
    raw = await ui.run_javascript(
        f"""(() => {{
            const element = document.getElementById('{PRODUCT_URL_INPUT_ID}');
            return element ? element.value : '';
        }})()"""
    )
    return str(raw or "")


async def _clear_product_url_input() -> None:
    await ui.run_javascript(
        f"""(() => {{
            const element = document.getElementById('{PRODUCT_URL_INPUT_ID}');
            if (element) {{
                element.value = '';
                element.focus();
            }}
        }})()"""
    )


def _render_text(tag: str, text: str, classes: str) -> None:
    with ui.element(tag).classes(classes):
        ui.html(escape(text))
