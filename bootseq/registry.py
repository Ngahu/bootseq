class Registry:
    def __init__(self):
        self._tasks = {}

    def register(self, fn=None, **kwargs):
        """
        Can be used as:
          @register
          @register()
          @register(order=10, tags={"core"})
        """
        if fn is None:
            # Case: @register(...)
            return lambda real_fn: self.register(real_fn, **kwargs)

        # Case: @register
        module = fn.__module__.split(".")[-1]
        namespace = kwargs.pop("namespace", module)
        name = kwargs.pop("name", fn.__name__)

        task_id = name if "." in name else f"{namespace}.{name}"

        if task_id in self._tasks:
            raise ValueError(f"Duplicate task: {task_id}")

        from .task import Task

        self._tasks[task_id] = Task(
            id=task_id,
            fn=fn,
            **kwargs,
        )

        return fn

    def all(self):
        return list(self._tasks.values())


default_registry = Registry()


def register(fn=None, **kwargs):
    """
    Public decorator bound to the default registry.
    """
    return default_registry.register(fn, **kwargs)
