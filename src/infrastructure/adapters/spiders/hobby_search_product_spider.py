from dataclasses import dataclass
from html import unescape
from re import DOTALL, IGNORECASE, Pattern, compile as re_compile, sub

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright
from scrapling import Selector

PRODUCT_DESCRIPTION_BLOCK_RE: Pattern[str] = re_compile(
    r"商品説明</h2>(?P<body>.*?)(?:<h2[^>]*>\s*商品仕様\s*</h2>)",
    IGNORECASE | DOTALL,
)
PRODUCT_REMOTE_ID_RE: Pattern[str] = re_compile(r"/(?P<remote_id>\d+)(?:[/?#].*)?$")
REQUEST_TIMEOUT_SECONDS = 30
PAGE_TIMEOUT_MS = REQUEST_TIMEOUT_SECONDS * 1000
PLAYWRIGHT_HEADLESS = False
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
)


@dataclass(frozen=True)
class ParsedHobbySearchProduct:
    thumbnail: str
    name: str
    category: list[str]
    price: str
    images_url: list[str]
    barcode: str
    code: str
    remote_id: str
    remote_url: str
    description: str


class HobbySearchProductSpider:
    name = "hobby_search_product"

    def crawl(self, url: str) -> ParsedHobbySearchProduct:
        html_bytes, encoding = _fetch_html(url)
        selector = Selector(content=html_bytes, url=url, encoding=encoding)

        category = _extract_category(selector)
        images_url = _extract_images(selector)
        thumbnail = _extract_thumbnail(selector, images_url)
        parsed_product = ParsedHobbySearchProduct(
            thumbnail=thumbnail,
            name=_extract_name(selector),
            category=category,
            price=_extract_price(selector),
            images_url=images_url,
            barcode=_extract_spec_value(selector, "JANコード"),
            code=_extract_spec_value(selector, "商品コード"),
            remote_id=_extract_remote_id(url),
            remote_url=url.strip(),
            description=_extract_description(selector),
        )
        _validate_parsed_product(parsed_product)
        return parsed_product


def _fetch_html(url: str) -> tuple[bytes, str]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=PLAYWRIGHT_HEADLESS)
        page = browser.new_page(
            user_agent=DEFAULT_USER_AGENT,
            locale="ja-JP",
        )
        page.set_default_timeout(PAGE_TIMEOUT_MS)
        try:
            page.goto(url, wait_until="domcontentloaded")
            _handle_age_gate(page)
            page.wait_for_selector("h1.c-product-detail__info-title")
            page.wait_for_selector(".c-product-detail__info-price-element")
            page.wait_for_selector("dt")
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except PlaywrightTimeoutError:
                pass
            html = page.content()
        finally:
            page.close()
            browser.close()
    return html.encode("utf-8"), "utf-8"


def _handle_age_gate(page: Page) -> None:
    age_gate_heading = page.locator("text=年齢確認")
    if age_gate_heading.count() == 0:
        return

    age_gate_target = page.locator("#__EVENTTARGET")
    age_gate_argument = page.locator("#__EVENTARGUMENT")
    age_gate_form = page.locator("#form1")
    if age_gate_target.count() == 0 or age_gate_argument.count() == 0 or age_gate_form.count() == 0:
        return

    page.evaluate(
        """() => {
            const target = document.getElementById('__EVENTTARGET');
            const argument = document.getElementById('__EVENTARGUMENT');
            const form = document.getElementById('form1');
            if (!target || !argument || !form) {
                return;
            }
            target.value = 'ctl00$masterBody$ctl03';
            argument.value = '';
            form.submit();
        }"""
    )
    page.wait_for_load_state("load")
    try:
        page.wait_for_load_state("networkidle", timeout=5000)
    except PlaywrightTimeoutError:
        pass


def _extract_category(selector: Selector) -> list[str]:
    category = [
        _normalize_text(text)
        for text in selector.css(".c-nav-breadcrumb__item [itemprop='name']::text").getall()
        if _normalize_text(text) != ""
    ]
    return _dedupe_preserving_order(category)


def _extract_images(selector: Selector) -> list[str]:
    image_urls = []
    for raw_src in selector.css(".c-product-detail__carousel-splide-slide-img img::attr(src)").getall():
        normalized_src = _normalize_text(raw_src)
        if normalized_src == "":
            continue
        image_urls.append(selector.urljoin(normalized_src))
    return _dedupe_preserving_order(image_urls)


def _extract_thumbnail(selector: Selector, images_url: list[str]) -> str:
    thumbnail_src = _normalize_text(selector.css("#masterBody_ulThumnail img::attr(src)").get())
    if thumbnail_src != "":
        return selector.urljoin(thumbnail_src)
    if not images_url:
        return ""
    return images_url[0]


def _extract_name(selector: Selector) -> str:
    return _normalize_text(selector.css("h1.c-product-detail__info-title::text").get())


def _extract_price(selector: Selector) -> str:
    price_element = selector.css(".c-product-detail__info-price-element")
    if not price_element:
        return ""
    return _normalize_text(price_element[0].get_all_text())


def _extract_spec_value(selector: Selector, label: str) -> str:
    value = selector.xpath(f"//dt[normalize-space()='{label}']/following-sibling::dd[1]/text()").get()
    return _normalize_text(value)


def _extract_remote_id(url: str) -> str:
    matched = PRODUCT_REMOTE_ID_RE.search(url.strip())
    if matched is None:
        return ""
    return matched.group("remote_id").strip()


def _extract_description(selector: Selector) -> str:
    block = selector.css(".c-page__container")
    for element in block:
        html_content = element.html_content
        if "商品説明" not in html_content or "商品仕様" not in html_content:
            continue
        matched = PRODUCT_DESCRIPTION_BLOCK_RE.search(html_content)
        if matched is None:
            continue
        description_html = matched.group("body")
        normalized_html = sub(r"<br\s*/?>", "\n", description_html, flags=IGNORECASE)
        normalized_html = sub(r"</p>|</div>", "\n", normalized_html, flags=IGNORECASE)
        normalized_html = sub(r"<[^>]+>", " ", normalized_html)
        return _normalize_text(normalized_html)
    return ""


def _validate_parsed_product(product: ParsedHobbySearchProduct) -> None:
    required_text_fields = {
        "thumbnail": product.thumbnail,
        "name": product.name,
        "price": product.price,
        "barcode": product.barcode,
        "code": product.code,
        "remote_id": product.remote_id,
        "remote_url": product.remote_url,
        "description": product.description,
    }
    empty_fields = [field_name for field_name, value in required_text_fields.items() if value.strip() == ""]
    if not product.category:
        empty_fields.append("category")
    if not product.images_url:
        empty_fields.append("images_url")

    if empty_fields:
        raise ValueError(f"Missing required product fields: {', '.join(empty_fields)}")


def _dedupe_preserving_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped_items: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        deduped_items.append(item)
    return deduped_items


def _normalize_text(value: object) -> str:
    normalized = unescape(str(value or ""))
    normalized = normalized.replace("\xa0", " ")
    return " ".join(normalized.split()).strip()
