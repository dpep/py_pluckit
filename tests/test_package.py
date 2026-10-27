import pluckit


def test_readme_imports():
    from pluckit import Pluckable, pluck
    from pluckit.pluckable import PluckableList

    assert pluck and Pluckable and PluckableList


def test_version():
    assert pluckit.__version__
