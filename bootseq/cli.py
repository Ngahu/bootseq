import argparse
import logging
from .registry import default_registry
from .runner import Runner
from .filters import Filters


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

    runner = Runner(
        default_registry,
        filters=filters,
        dry_run=args.dry_run or args.command == "plan",
        max_workers=args.max_workers,
    )

    runner.run()
