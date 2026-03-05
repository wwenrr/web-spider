from adapters.spiders.base_spider import BaseSpider


class CrawlService:
    def __init__(self, spider: BaseSpider) -> None:
        self.spider = spider

    def run(self, url: str) -> list[dict[str, object]]:
        return self.spider.crawl(url)
