from infrastructure.queues.task_registry import resolve_task


class PybgworkerQueue:
    def enqueue(self, task_name: str, *args: object, **kwargs: object) -> None:
        fn = resolve_task(task_name)
        delay = getattr(fn, "delay", None)
        if callable(delay):
            delay(*args, **kwargs)
            return
        fn(*args, **kwargs)
