import pluckit


def test_exports():
    assert {"pluck", "Pluckable", "PluckableList"} <= set(pluckit.__all__)

    for name in pluckit.__all__:
        assert getattr(pluckit, name)


def test_version():
    assert pluckit.__version__
