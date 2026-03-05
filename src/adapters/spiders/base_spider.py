from abc import ABC, abstractmethod

class BaseSpider(ABC):
    name: str = "base"

    @abstractmethod
    def crawl(self, url: str) -> list[dict[str, object]]:
        raise NotImplementedError
