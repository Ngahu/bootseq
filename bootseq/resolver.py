from .exceptions import DependencyError


def resolve(tasks):
    graph = {t.id: t for t in tasks}
    resolved, visiting = [], set()

    def visit(task):
        if task.id in visiting:
            raise DependencyError(f"Circular dependency: {task.id}")

        if task in resolved:
            return

        visiting.add(task.id)
        for dep in task.requires:
            if dep not in graph:
                raise DependencyError(f"Missing dependency: {dep}")
            visit(graph[dep])
        visiting.remove(task.id)
        resolved.append(task)

    for task in sorted(tasks, key=lambda t: t.order):
        visit(task)

    return resolved
