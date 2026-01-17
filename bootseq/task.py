from dataclasses import dataclass, field
from typing import Callable, Set, Optional


@dataclass(frozen=True)
class Task:
    id: str
    fn: Callable
    order: int = 100
    requires: Set[str] = field(default_factory=set)
    tags: Set[str] = field(default_factory=set)
    parallel_safe: bool = True
    rollback: Optional[Callable] = None
