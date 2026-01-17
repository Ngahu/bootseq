import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from .resolver import resolve

log = logging.getLogger("bootseq")


class Runner:
    def __init__(
        self,
        registry,
        *,
        filters=None,
        dry_run=False,
        max_workers=4,
        fail_fast=True,
    ):
        self.registry = registry
        self.filters = filters
        self.dry_run = dry_run
        self.max_workers = max_workers
        self.fail_fast = fail_fast

    def run(self):
        tasks = resolve(self.registry.all())
        if self.filters:
            tasks = [t for t in tasks if self.filters.allow(t)]

        completed = []

        try:
            for batch in self._batches(tasks):
                with ThreadPoolExecutor(self.max_workers) as pool:
                    futures = {pool.submit(self._run_task, t): t for t in batch}
                    for f in as_completed(futures):
                        f.result()
                        completed.append(futures[f])
        except Exception:
            self._rollback(completed)
            raise

    def _run_task(self, task):
        log.info("→ %s", task.id)
        if not self.dry_run:
            task.fn()

    def _rollback(self, completed):
        for task in reversed(completed):
            if task.rollback:
                try:
                    task.rollback()
                except Exception:
                    log.exception("Rollback failed: %s", task.id)

    def _batches(self, tasks):
        batch = []
        for task in tasks:
            if not task.parallel_safe and batch:
                yield batch
                batch = []
            batch.append(task)
        if batch:
            yield batch
