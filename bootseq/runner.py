import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
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
        show_progress=True,
    ):
        self.registry = registry
        self.filters = filters
        self.dry_run = dry_run
        self.max_workers = max_workers
        self.fail_fast = fail_fast
        self.show_progress = show_progress

    def run(self):
        tasks = resolve(self.registry.all())
        if self.filters:
            tasks = [t for t in tasks if self.filters.allow(t)]

        if not tasks:
            log.info("No tasks to run.")
            return

        completed = []
        total_tasks = len(tasks)

        # Create progress bar
        desc = "[DRY-RUN] Simulating" if self.dry_run else "Running tasks"
        pbar = tqdm(
            total=total_tasks,
            desc=desc,
            unit="task",
            disable=not self.show_progress,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        )

        try:
            for batch in self._batches(tasks):
                with ThreadPoolExecutor(self.max_workers) as pool:
                    futures = {pool.submit(self._run_task, t, pbar): t for t in batch}
                    for f in as_completed(futures):
                        f.result()
                        completed.append(futures[f])
                        pbar.update(1)
        except Exception:
            pbar.close()
            self._rollback(completed)
            raise
        finally:
            pbar.close()

    def _run_task(self, task, pbar):
        pbar.set_postfix_str(task.id, refresh=True)
        if self.dry_run:
            log.info("[DRY-RUN] → %s", task.id)
        else:
            log.debug("→ %s", task.id)
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
