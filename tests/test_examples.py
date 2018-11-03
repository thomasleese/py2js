from pathlib import Path

import pytest

from py2js.compiler import compile


def load_test_cases():
    path = Path(__file__).parent / 'examples'

    test_cases = path.iterdir()

    return test_cases


test_cases = load_test_cases()


@pytest.mark.parametrize('filename', test_cases)
def test_compiles(filename):
    assert compile(filename)
