from typing import Protocol


class ICategoryCrawlQueue(Protocol):
    def enqueue(self, task_name: str, *args: object, **kwargs: object) -> None: ...
