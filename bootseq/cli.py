import argparse
import logging
from .registry import default_registry
from .runner import Runner
from .filters import Filters
from .resolver import resolve


def plan_tasks(registry, filters=None):
    """List all registered tasks in execution order."""
    tasks = resolve(registry.all())
    if filters:
        tasks = [t for t in tasks if filters.allow(t)]

    if not tasks:
        print("No tasks registered.")
        return

    print(f"\n{'ID':<40} {'Order':<8} {'Tags':<20} {'Requires'}")
    print("-" * 90)
    for task in tasks:
        tags = ", ".join(task.tags) if task.tags else "-"
        requires = ", ".join(task.requires) if task.requires else "-"
        print(f"{task.id:<40} {task.order:<8} {tags:<20} {requires}")
    print(f"\nTotal: {len(tasks)} task(s)\n")


def main():
    parser = argparse.ArgumentParser("bootseq")
    parser.add_argument("command", choices=["run", "plan"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--skip", nargs="*")
    parser.add_argument("--tags", nargs="*")
    parser.add_argument("--max-workers", type=int, default=4)

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    filters = Filters(
        only=args.only,
        skip=args.skip,
        tags=args.tags,
    )

    if args.command == "plan":
        plan_tasks(default_registry, filters)
        return

    runner = Runner(
        default_registry,
        filters=filters,
        dry_run=args.dry_run or args.command == "plan",
        max_workers=args.max_workers,
    )

    runner.run()
