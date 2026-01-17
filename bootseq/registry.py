from .task import Task


class Registry:
    def __init__(self):
        self._tasks = {}

    def register(self, **kwargs):
        def decorator(fn):
            module = fn.__module__.split(".")[-1]
            namespace = kwargs.pop("namespace", module)
            name = kwargs.pop("name", fn.__name__)

            task_id = name if "." in name else f"{namespace}.{name}"

            if task_id in self._tasks:
                raise ValueError(f"Duplicate task: {task_id}")

            self._tasks[task_id] = Task(
                id=task_id,
                fn=fn,
                **kwargs,
            )
            return fn

        return decorator

    def all(self):
        return list(self._tasks.values())


default_registry = Registry()


def register(**kwargs):
    return default_registry.register(**kwargs)
