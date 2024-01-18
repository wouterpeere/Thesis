import pytest


def test_main():
    from Main import run
    run()
    assert 1==1