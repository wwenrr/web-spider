from infrastructure.adapters.spiders.base_spider import BaseSpider


class TikiSpider(BaseSpider):
    name = "tiki"

    def crawl(self, url: str) -> list[dict[str, object]]:
        return [
            {
                "source": self.name,
                "url": url,
                "title": "Tiki sample result",
                "payload": {"status": "ok"},
            }
        ]
