import pytest


def test_main():
    from Experiment.Main  import run
    run()
    assert 1==1