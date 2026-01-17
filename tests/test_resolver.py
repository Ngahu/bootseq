from bootseq.resolver import resolve
from bootseq.task import Task


def test_dependency_order():
    t1 = Task(id="a", fn=lambda: None)
    t2 = Task(id="b", fn=lambda: None, requires={"a"})
    ordered = resolve([t2, t1])
    assert [t.id for t in ordered] == ["a", "b"]
