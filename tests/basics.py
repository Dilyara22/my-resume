import pytest

@pytest.mark.smoke
def test_basics1():
    assert 1==1, 'Did not match'

@pytest.mark.regression
def test_basics2():
    assert 2==3, 'Did not match'

@pytest.mark.skip
def test_basics3():
    assert 'a'=='A', 'Did not match'
