from typing import Protocol


class ISpider(Protocol):
    def crawl(self, url: str) -> list[dict]: ...
