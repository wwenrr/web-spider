from typing import Protocol


class IJobQueue(Protocol):
    def enqueue(self, task_name: str, *args: object, **kwargs: object) -> None: ...
