import fnmatch


class Filters:
    def __init__(self, *, only=None, skip=None, tags=None):
        self.only = set(only or [])
        self.skip = set(skip or [])
        self.tags = set(tags or [])

    def allow(self, task):
        if self.only and not any(fnmatch.fnmatch(task.id, p) for p in self.only):
            return False

        if any(fnmatch.fnmatch(task.id, p) for p in self.skip):
            return False

        if self.tags and not (self.tags & task.tags):
            return False

        return True
