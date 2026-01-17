from bootseq.registry import Registry


def test_register():
    r = Registry()

    @r.register()
    def foo():
        pass

    assert len(r.all()) == 1
