from infrastructure.adapters.spiders.base_spider import BaseSpider


class ShopeeSpider(BaseSpider):
    name = "shopee"

    def crawl(self, url: str) -> list[dict[str, object]]:
        return [
            {
                "source": self.name,
                "url": url,
                "title": "Shopee sample result",
                "payload": {"status": "ok"},
            }
        ]
