from bootseq.registry import Registry
from bootseq.runner import Runner


def test_runner_executes():
    r = Registry()
    executed = []

    @r.register()
    def task():
        executed.append(True)

    Runner(r).run()
    assert executed == [True]
