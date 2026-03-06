from dataclasses import dataclass
from math import ceil
from re import Pattern, compile as re_compile
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen

from scrapling import Selector

CATEGORY_PAGE_TIMEOUT_SECONDS = 30
CATEGORY_PAGE_URL_RE: Pattern[str] = re_compile(r"^\d+$")
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
)


@dataclass(frozen=True)
class ParsedHobbySearchCategory:
    category_name: str
    total_products: int
    products_per_page: int
    total_pages: int
    product_urls: list[str]


class HobbySearchCategorySpider:
    name = "hobby_search_category"

    def crawl(self, category_url: str) -> ParsedHobbySearchCategory:
        first_page_selector = _fetch_selector(category_url)
        category_name = _extract_category_name(first_page_selector)
        total_products = _extract_total_products(first_page_selector)
        first_page_urls = _extract_product_urls(first_page_selector)
        products_per_page = len(first_page_urls)
        if products_per_page < 1:
            raise ValueError("Could not read products per page from category page.")

        total_pages = ceil(total_products / products_per_page)
        product_urls = list(first_page_urls)
        for page_number in range(2, total_pages + 1):
            page_selector = _fetch_selector(_build_page_url(category_url, page_number))
            page_urls = _extract_product_urls(page_selector)
            if not page_urls:
                raise ValueError(f"Could not read product URLs on category page {page_number}.")
            product_urls.extend(page_urls)

        return ParsedHobbySearchCategory(
            category_name=category_name,
            total_products=total_products,
            products_per_page=products_per_page,
            total_pages=total_pages,
            product_urls=_dedupe_preserving_order(product_urls),
        )


def _fetch_selector(url: str) -> Selector:
    request = Request(url=url, headers={"User-Agent": DEFAULT_USER_AGENT})
    with urlopen(request, timeout=CATEGORY_PAGE_TIMEOUT_SECONDS) as response:
        payload = response.read()
        encoding = response.headers.get_content_charset() or "utf-8"
    return Selector(content=payload, url=url, encoding=encoding)


def _extract_category_name(selector: Selector) -> str:
    breadcrumb_items = [
        _normalize_text(text)
        for text in selector.css(".c-nav-breadcrumb__item [itemprop='name']::text").getall()
        if _normalize_text(text) != ""
    ]
    if not breadcrumb_items:
        raise ValueError("Could not read category name from category page.")
    return breadcrumb_items[-1]


def _extract_total_products(selector: Selector) -> int:
    raw_total = _normalize_text(selector.css("#masterBody_ItemList_totalHitsaCntSp::text").get())
    digits_only = "".join(character for character in raw_total if character.isdigit())
    if digits_only == "":
        raise ValueError("Could not read total products from category page.")
    return int(digits_only)


def _extract_product_urls(selector: Selector) -> list[str]:
    product_urls: list[str] = []
    for raw_href in selector.css(".c-product-list__item a.c-card__th-links::attr(href)").getall():
        normalized_href = _normalize_text(raw_href)
        if normalized_href == "":
            continue
        product_urls.append(selector.urljoin(normalized_href))
    return _dedupe_preserving_order(product_urls)


def _build_page_url(category_url: str, page_number: int) -> str:
    parts = urlsplit(category_url)
    path_segments = [segment for segment in parts.path.rstrip("/").split("/") if segment != ""]
    if not path_segments or not CATEGORY_PAGE_URL_RE.match(path_segments[-1]):
        raise ValueError(f"Could not build paginated URL from category URL: {category_url}")
    path_segments[-1] = str(page_number)
    return urlunsplit((parts.scheme, parts.netloc, f"/{'/'.join(path_segments)}", parts.query, ""))


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
    return " ".join(str(value or "").replace("\xa0", " ").split()).strip()
